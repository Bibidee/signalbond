import fs from "node:fs/promises";
import { Wallet } from "ethers";
import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { privateKeyToAccount } from "viem/accounts";
const wallet = await Wallet.fromEncryptedJson(await fs.readFile(process.env.SIGNALBOND_KEYSTORE, "utf8"), process.env.SIGNALBOND_WALLET_PASSWORD);
const client = createClient({ chain: studionet, endpoint: process.env.SIGNALBOND_RPC || "https://studio.genlayer.com/api", account: privateKeyToAccount(wallet.privateKey) });
const tx = await client.writeContract({ address: process.env.SIGNALBOND_ADDRESS, functionName: "challenge_claim", args: [process.env.SIGNALBOND_ID, "", "", ""], value: 10000000000000000n, consensusMaxRotations: 5 });
console.log(JSON.stringify({ challenger: wallet.address, tx }, null, 2));
