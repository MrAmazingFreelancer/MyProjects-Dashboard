import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const response = await openai.responses.create({
  model: "gpt-5.4-mini",
  input: "Write a haiku about AI.",
});

console.log(response.output_text);
