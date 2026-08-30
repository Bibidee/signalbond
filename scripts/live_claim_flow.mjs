import fs from "node:fs/promises";
import crypto from "node:crypto";
import { setTimeout as delay } from "node:timers/promises";
import { Wallet } from "ethers";
import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";
const wallet = await Wallet.fromEncryptedJson(await fs.readFile(process.env.SIGNALBOND_KEYSTORE, "utf8"), process.env.SIGNALBOND_WALLET_PASSWORD);
const client = createClient({ chain: studionet, endpoint: process.env.SIGNALBOND_RPC || "https://studio.genlayer.com/api", account: privateKeyToAccount(wallet.privateKey) });
const url = process.env.SIGNALBOND_EVIDENCE_URL;
const bytes = Buffer.from(await (await fetch(url)).arrayBuffer());
const hash = "0x" + crypto.createHash("sha256").update(bytes).digest("hex");
const id = process.env.SIGNALBOND_ID;
const submit = await client.writeContract({ address: process.env.SIGNALBOND_ADDRESS, functionName: "submit_claim", args: [id, wallet.address, process.env.SIGNALBOND_STATEMENT, url, hash, 3600], value: 1000000000000000000n, consensusMaxRotations: 5 });
console.log(JSON.stringify({ submit, id, hash }, null, 2));
for (;;) { const t = await client.getTransaction({ hash: submit }); if (["FINALIZED","UNDETERMINED","CANCELED"].includes(t.statusName)) break; await delay(6000); }
const review = await client.writeContract({ address: process.env.SIGNALBOND_ADDRESS, functionName: "review_claim", args: [id], consensusMaxRotations: 5 });
console.log(JSON.stringify({ review }, null, 2));
for (;;) { const t = await client.getTransaction({ hash: review }); if (["FINALIZED","UNDETERMINED","CANCELED"].includes(t.statusName)) { console.log(JSON.stringify({ status: t.statusName, result: t.result_name, execution: t.consensus_data?.leader_receipt?.[0]?.execution_result }, null, 2)); break; } await delay(6000); }
