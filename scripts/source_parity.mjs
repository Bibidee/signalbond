import fs from "node:fs/promises";
import crypto from "node:crypto";
import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

const client = createClient({ chain: studionet, endpoint: process.env.SIGNALBOND_RPC || "https://studio.genlayer.com/api" });
const address = process.env.SIGNALBOND_ADDRESS;
const local = await fs.readFile("contracts/signalbond.py");
const deployed = await client.getContractCode(address);
const bytes = Buffer.from(deployed, "utf8");
const digest = value => crypto.createHash("sha256").update(value).digest("hex");
console.log(JSON.stringify({ local_sha256: digest(local), deployed_sha256: digest(bytes), byte_equal: local.equals(bytes), deployed_bytes: bytes.length, local_bytes: local.length }, null, 2));
