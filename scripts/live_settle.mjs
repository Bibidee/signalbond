import fs from "node:fs/promises";
import { Wallet } from "ethers";
import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";
const wallet = await Wallet.fromEncryptedJson(await fs.readFile(process.env.SIGNALBOND_KEYSTORE, "utf8"), process.env.SIGNALBOND_WALLET_PASSWORD);
const client = createClient({ chain: studionet, endpoint: process.env.SIGNALBOND_RPC || "https://studio.genlayer.com/api", account: privateKeyToAccount(wallet.privateKey) });
const tx = await client.writeContract({ address: process.env.SIGNALBOND_ADDRESS, functionName: "settle_claim", args: [process.env.SIGNALBOND_ID], consensusMaxRotations: 5 });
console.log(tx);
