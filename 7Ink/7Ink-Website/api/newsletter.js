function parseUrlEncoded(rawBody) {
  const out = {};
  const params = new URLSearchParams(rawBody || '');
  for (const [key, value] of params.entries()) {
    out[key] = value;
  }
  return out;
}

function readRawBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk.toString();
    });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

async function sendViaWebhook(url, payload) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error('Webhook delivery failed');
  }
}

async function sendViaResend(email) {
  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.NEWSLETTER_TO || process.env.CONTACT_TO;
  const from = process.env.CONTACT_FROM || 'website@7ink.com.au';

  if (!apiKey || !to) {
    return;
  }

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from,
      to,
      subject: 'New Newsletter Subscription',
      html: `<p><strong>Email:</strong> ${email}</p>`
    })
  });

  if (!response.ok) {
    throw new Error('Resend delivery failed');
  }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).send('Method Not Allowed');
    return;
  }

  try {
    const rawBody = await readRawBody(req);
    const data = parseUrlEncoded(rawBody);

    if (!data.email) {
      res.status(400).send('Email is required');
      return;
    }

    const payload = {
      type: 'newsletter',
      email: data.email,
      ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress || ''
    };

    if (process.env.CONTACT_WEBHOOK_URL) {
      await sendViaWebhook(process.env.CONTACT_WEBHOOK_URL, payload);
    }

    await sendViaResend(data.email);

    res.status(200).send('OK');
  } catch (error) {
    console.error(error);
    res.status(500).send('Unable to subscribe right now');
  }
};
