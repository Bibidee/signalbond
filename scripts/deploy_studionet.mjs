import fs from "node:fs/promises";
import { Wallet } from "ethers";
import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";

const keystore = process.env.SIGNALBOND_KEYSTORE;
const password = process.env.SIGNALBOND_WALLET_PASSWORD;
if (!keystore || !password) throw new Error("SIGNALBOND_KEYSTORE and SIGNALBOND_WALLET_PASSWORD are required");
const wallet = await Wallet.fromEncryptedJson(await fs.readFile(keystore, "utf8"), password);
const client = createClient({ chain: studionet, endpoint: process.env.SIGNALBOND_RPC || "https://studio.genlayer.com/api", account: privateKeyToAccount(wallet.privateKey) });
const code = await fs.readFile("contracts/signalbond.py", "utf8");
const hash = await client.deployContract({ code, args: [wallet.address], consensusMaxRotations: 5 });
console.log(JSON.stringify({ deploymentTransaction: hash, owner: wallet.address }, null, 2));
