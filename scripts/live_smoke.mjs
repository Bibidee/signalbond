import fs from "node:fs/promises";
import crypto from "node:crypto";
import { Wallet } from "ethers";
import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";

const address = process.env.SIGNALBOND_ADDRESS;
const keystore = process.env.SIGNALBOND_KEYSTORE;
const password = process.env.SIGNALBOND_WALLET_PASSWORD;
if (!address || !keystore || !password) throw new Error("SIGNALBOND_ADDRESS, SIGNALBOND_KEYSTORE and SIGNALBOND_WALLET_PASSWORD are required");
const wallet = await Wallet.fromEncryptedJson(await fs.readFile(keystore, "utf8"), password);
const client = createClient({ chain: studionet, endpoint: process.env.SIGNALBOND_RPC || "https://studio.genlayer.com/api", account: privateKeyToAccount(wallet.privateKey) });
const body = await (await fetch("https://raw.githubusercontent.com/Bibidee/signalbond/790c080684697f2226ae5422d89fa19bb4766161/README.md")).arrayBuffer();
const hash = "0x" + crypto.createHash("sha256").update(Buffer.from(body)).digest("hex");
const url = "https://raw.githubusercontent.com/Bibidee/signalbond/790c080684697f2226ae5422d89fa19bb4766161/README.md";
const tx = await client.writeContract({ address, functionName: "submit_claim", args: ["live-safe-001", wallet.address, "SignalBond is a reusable claim-verification primitive", url, hash, 3600], value: 1000000000000000000n, consensusMaxRotations: 5 });
console.log(JSON.stringify({ wallet: wallet.address, submit: tx, evidence_url: url, evidence_hash: hash }, null, 2));
