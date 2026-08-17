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

function parseBody(rawBody) {
  if (!rawBody) {
    return {};
  }

  try {
    return JSON.parse(rawBody);
  } catch (error) {
    const out = {};
    const params = new URLSearchParams(rawBody);
    for (const [key, value] of params.entries()) {
      out[key] = value;
    }
    return out;
  }
}

function writeJson(res, statusCode, payload) {
  res.status(statusCode);
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify(payload));
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    writeJson(res, 405, { error: 'Method Not Allowed' });
    return;
  }

  const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
  const apiToken = process.env.CLOUDFLARE_STREAM_API_TOKEN;

  if (!accountId || !apiToken) {
    writeJson(res, 500, {
      error: 'Missing required server environment variables: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_STREAM_API_TOKEN'
    });
    return;
  }

  try {
    const rawBody = await readRawBody(req);
    const data = parseBody(rawBody);

    const requestedMaxDuration = Number(data.maxDurationSeconds);
    const maxDurationSeconds = Number.isFinite(requestedMaxDuration) && requestedMaxDuration > 0
      ? Math.floor(requestedMaxDuration)
      : 3600;

    const directUploadPayload = {
      maxDurationSeconds
    };

    if (typeof data.requireSignedURLs === 'boolean') {
      directUploadPayload.requireSignedURLs = data.requireSignedURLs;
    } else if (data.requireSignedURLs === 'true' || data.requireSignedURLs === 'false') {
      directUploadPayload.requireSignedURLs = data.requireSignedURLs === 'true';
    }

    if (typeof data.expiry === 'string' && data.expiry.trim()) {
      directUploadPayload.expiry = data.expiry.trim();
    }

    const meta = {};
    if (typeof data.filename === 'string' && data.filename.trim()) {
      meta.filename = data.filename.trim();
    }
    if (typeof data.title === 'string' && data.title.trim()) {
      meta.title = data.title.trim();
    }
    if (Object.keys(meta).length) {
      directUploadPayload.meta = meta;
    }

    const cloudflareResponse = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${accountId}/stream/direct_upload`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${apiToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(directUploadPayload)
      }
    );

    const responseText = await cloudflareResponse.text();
    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch (_error) {
      responseData = null;
    }

    if (!cloudflareResponse.ok || !responseData || !responseData.success || !responseData.result) {
      writeJson(res, 502, {
        error: 'Unable to create direct upload URL',
        status: cloudflareResponse.status,
        details: responseData || responseText || null
      });
      return;
    }

    writeJson(res, 200, {
      uploadURL: responseData.result.uploadURL,
      uid: responseData.result.uid,
      maxDurationSeconds
    });
  } catch (error) {
    console.error(error);
    writeJson(res, 500, { error: 'Unexpected error while creating upload URL' });
  }
};
