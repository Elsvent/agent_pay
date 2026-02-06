# CLAUDE.md - agent_pay

## Project Overview

Hybrid blockchain project combining Solidity smart contracts, Hardhat-based testing/deployment (TypeScript), and a Python-based Circle wallet integration. Supports Ethereum L1 (Sepolia testnet) and Optimism L2 chains.

## Repository Structure

```
agent_pay/
├── contracts/              # Solidity smart contracts
│   ├── Counter.sol         # Main contract (state mgmt + events)
│   └── Counter.t.sol       # Foundry/forge-std test suite
├── ignition/
│   └── modules/
│       └── Counter.ts      # Hardhat Ignition deployment module
├── scripts/
│   └── send-op-tx.ts       # OP chain transaction example
├── test/
│   └── Counter.ts          # Hardhat/Viem test suite (node:test)
├── wallet/                 # Python Circle wallet integration
│   ├── main.py             # Circle Developer-Controlled Wallets API
│   ├── pyproject.toml      # Python project config (uv)
│   ├── uv.lock             # Dependency lock file
│   └── .python-version     # Python 3.13
├── hardhat.config.ts       # Hardhat configuration
├── tsconfig.json           # TypeScript config
└── package.json            # Node.js project (ES modules)
```

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Smart Contracts | Solidity | 0.8.28 |
| Build/Test Framework | Hardhat | 3.x |
| Web3 Library | Viem | (via hardhat-toolbox-viem) |
| Deployment | Hardhat Ignition | - |
| TypeScript | ES2022 target, Node16 modules | strict mode |
| Node.js | 22+ | ES modules (`"type": "module"`) |
| Package Manager (JS) | pnpm | 10.x |
| Python | 3.13+ | - |
| Package Manager (Python) | uv | - |
| Wallet SDK | circle-developer-controlled-wallets | 9.2.0+ |

## Common Commands

### JavaScript/TypeScript (Hardhat)

```bash
# Install dependencies
pnpm install

# Compile contracts
npx hardhat compile

# Run Hardhat/Viem tests
npx hardhat test

# Run a script
npx hardhat run scripts/send-op-tx.ts

# Deploy via Ignition
npx hardhat ignition deploy ignition/modules/Counter.ts

# Compile with production optimizations
npx hardhat compile --profile production
```

### Python (Wallet)

```bash
# Install Python dependencies (from wallet/ directory)
cd wallet && uv sync

# Run wallet integration
python wallet/main.py
```

## Network Configuration

Defined in `hardhat.config.ts`:

- **hardhatMainnet** - EDR-simulated L1 chain (local, default for tests)
- **hardhatOp** - EDR-simulated OP chain (local, for L2 scripts)
- **sepolia** - Ethereum Sepolia testnet (requires `SEPOLIA_RPC_URL` and `SEPOLIA_PRIVATE_KEY` env vars via `configVariable()`)

## Environment Variables

| Variable | Used By | Purpose |
|----------|---------|---------|
| `SEPOLIA_RPC_URL` | hardhat.config.ts | RPC endpoint for Sepolia testnet |
| `SEPOLIA_PRIVATE_KEY` | hardhat.config.ts | Account private key for Sepolia |

These are accessed via Hardhat's `configVariable()` and only needed when deploying to Sepolia.

## Code Conventions

### Solidity

- License: `UNLICENSED`
- Pragma: `^0.8.28`
- State variables: `uint public x` (public visibility for auto-getter)
- Events: PascalCase (`event Increment(uint by)`)
- Functions: camelCase (`inc()`, `incBy()`)
- Input validation: `require()` with descriptive messages
- Emit events after state changes

### TypeScript

- ES module imports (`import ... from`)
- Tests use `node:test` (`describe`/`it`) and `node:assert/strict`
- Async patterns with top-level `await` in scripts
- BigInt notation for values (`5n`, `1n`)
- Viem client pattern: `publicClient` for reads, `walletClient`/`senderClient` for writes

### Python

- snake_case function names
- `from circle.web3 import utils` import style
- `if __name__ == "__main__"` entry point pattern

## Testing

Two test suites exist:

1. **Foundry tests** (`contracts/Counter.t.sol`):
   - Extends `forge-std/Test.sol`
   - `setUp()` for initialization
   - `test_` prefix for unit tests, `testFuzz_` for fuzz tests
   - `vm.expectRevert()` for revert testing

2. **Hardhat/Viem tests** (`test/Counter.ts`):
   - `describe`/`it` blocks with `node:test`
   - `viem.deployContract()` to deploy in tests
   - `viem.assertions.emitWithArgs()` for event verification
   - `publicClient.getContractEvents()` for event querying
   - Run with `npx hardhat test`

## Deployment

Hardhat Ignition modules in `ignition/modules/`. The `CounterModule`:
1. Deploys the Counter contract
2. Calls `incBy(5n)` post-deployment
3. Returns the counter instance

## Solidity Compiler Profiles

- **default**: Solidity 0.8.28, no optimizer (faster compilation for dev)
- **production**: Solidity 0.8.28, optimizer enabled (200 runs)

## Key Patterns

- Contracts emit events for all state changes (important for off-chain indexing)
- Tests verify both state and event correctness
- Scripts demonstrate multi-chain patterns (L1 gas estimation on L2)
- Wallet integration is a separate Python module using Circle's managed wallet service

## Security Notes

- Never commit private keys or API secrets to the repository
- Use Hardhat's `configVariable()` for sensitive configuration
- The wallet module currently has hardcoded test API keys - these should be moved to environment variables for production
