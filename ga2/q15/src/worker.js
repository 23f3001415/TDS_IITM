const EMAIL = "23f3001415@ds.study.iitm.ac.in";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

function jsonResponse(status, payload) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(),
    },
  });
}

function reverseByType(type, value) {
  if (type === "string") {
    return String(value).split("").reverse().join("");
  }

  if (type === "array") {
    if (!Array.isArray(value)) {
      throw new Error("value must be an array for type=array");
    }
    return [...value].reverse();
  }

  if (type === "words") {
    return String(value).trim().split(/\s+/).reverse().join(" ");
  }

  if (type === "number") {
    const num = Number(value);
    if (!Number.isFinite(num) || !Number.isInteger(num)) {
      throw new Error("value must be an integer for type=number");
    }
    const sign = num < 0 ? -1 : 1;
    const digits = String(Math.abs(num));
    const reversed = digits.split("").reverse().join("");
    return sign * parseInt(reversed.replace(/^0+/, "") || "0", 10);
  }

  throw new Error("unsupported type");
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (request.method !== "POST" || url.pathname !== "/data") {
      return jsonResponse(404, { error: "Not Found" });
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return jsonResponse(400, { error: "Invalid JSON" });
    }

    const { type, value } = body || {};

    try {
      const reversed = reverseByType(type, value);
      return jsonResponse(200, {
        reversed,
        email: EMAIL,
      });
    } catch (err) {
      return jsonResponse(400, { error: err.message });
    }
  },
};
