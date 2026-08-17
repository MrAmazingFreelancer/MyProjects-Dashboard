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

async function sendViaResend(payload) {
  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.CONTACT_TO;
  const from = process.env.CONTACT_FROM || 'website@7ink.com.au';

  if (!apiKey || !to) {
    return;
  }

  const html = [
    '<h2>New Contact Submission</h2>',
    `<p><strong>Name:</strong> ${payload.name || ''}</p>`,
    `<p><strong>Email:</strong> ${payload.email || ''}</p>`,
    `<p><strong>Subject:</strong> ${payload.subject || ''}</p>`,
    `<p><strong>Message:</strong><br>${(payload.message || '').replace(/\n/g, '<br>')}</p>`
  ].join('');

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from,
      to,
      subject: `Website Contact: ${payload.subject || 'No subject'}`,
      html
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

    if (!data.name || !data.email || !data.subject || !data.message) {
      res.status(400).send('Missing required fields');
      return;
    }

    const payload = {
      type: 'contact',
      name: data.name,
      email: data.email,
      subject: data.subject,
      message: data.message,
      ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress || ''
    };

    if (process.env.CONTACT_WEBHOOK_URL) {
      await sendViaWebhook(process.env.CONTACT_WEBHOOK_URL, payload);
    }

    await sendViaResend(payload);

    res.status(200).send('OK');
  } catch (error) {
    console.error(error);
    res.status(500).send('Unable to send message right now');
  }
};
