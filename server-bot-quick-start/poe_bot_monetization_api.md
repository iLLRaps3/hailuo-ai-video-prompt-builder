# Poe Bot Monetization API Documentation

## Overview

The Poe Bot Monetization API allows bot creators to implement variable pricing for their bots. Instead of charging a fixed price per message within the Poe website, you can dynamically price your bot's responses based on factors such as input length, output length, or computational complexity.

The API provides two main functions:

- **Authorize:** Reserve potential costs before providing the service.
- **Capture:** Actually charge the user after providing the service.

## Key Concepts

### Cost Items

Costs are specified using `CostItem` objects that contain:

- `amount_usd_milli_cents` (int): The cost in thousandths of a US cent.
- `description` (Optional[str]): Optional description of what the cost is for. This should be clear enough to be user-facing.

> **Note:** Amounts are in integer format to avoid floating point precision issues.

### Rate Cards

You can define a rate card in your bot settings to explain your pricing structure to users. The rate card supports markdown formatting and special tags to display prices. By using the tag `[usd_milli_cents=X]`, X will be converted into the applicable compute points value.

### Cost Label

You can define a cost label in your bot settings to provide a concise description of your bot's cost. The cost label should be a short string that clearly communicates how users are charged. By using the tag `[usd_milli_cents=X]`, X will be converted into the applicable compute points value.

## Implementation Steps

### 1. Prerequisites

- Be enrolled in Poe revenue sharing.
- Use the latest version of `fastapi_poe`.

### 2. Implement Cost Authorization

Before processing expensive operations, authorize the potential cost:

```python
await self.authorize_cost(
    request,
    fp.CostItem(
        amount_usd_milli_cents=estimated_cost,
        description="Processing fee"
    )
)
```

### 3. Implement Cost Capture

After providing the service, capture the actual cost:

```python
await self.capture_cost(
    request,
    fp.CostItem(
        amount_usd_milli_cents=actual_cost,
        description="Processing fee"
    )
)
```

### 4. Define Your Rate Card and Cost Label

Override the `get_settings` method to specify your pricing structure:

```python
async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
    rate_card = (
        "Cost overview: \n\n"
        "| Type | Rate |\n"
        "|------|------|\n"
        "| Input (text) | [usd_milli_cents=10] points / 1k tokens |\n"
        "| Input (image) | [usd_milli_cents=10] points / 1k pixels |\n"
    )
    cost_label = "[usd_milli_cents=30]+"
    return fp.SettingsResponse(rate_card=rate_card, cost_label=cost_label)
```

## Examples

### Basic Implementation

```python
async def get_response(self, request: fp.QueryRequest) -> AsyncIterable[fp.PartialResponse]:
    # Calculate estimated cost (dummy)
    input_tokens = await self._get_num_tokens(request.query)
    estimated_cost = input_tokens * COST_PER_TOKEN

    # Authorize estimated cost
    await self.authorize_cost(request,
        fp.CostItem(
            amount_usd_milli_cents=estimated_cost,
            description="Processing fee"
        )
    )

    # Process request (dummy)
    response = await self._process_query(request.query)

    # Capture actual cost
    actual_cost = len(response) * COST_PER_TOKEN
    await self.capture_cost(request,
        fp.CostItem(
            amount_usd_milli_cents=actual_cost,
            description="Processing fee"
        )
    )

    yield fp.PartialResponse(text=response)
```

### Multiple Cost Items

```python
costs = [
    fp.CostItem(amount_usd_milli_cents=1000, description="Base fee"),
    fp.CostItem(amount_usd_milli_cents=5000, description="Processing fee")
]
await self.authorize_cost(request, costs)
```

## Best Practices

- **Authorize Early and Accurately:** Try to authorize costs at the beginning of processing to avoid wasting resources. Make your cost estimates as accurate as possible to avoid over-authorizing (users may not have enough points) or under-authorizing (you may not be paid fully).
- **Clear Documentation:** Use the rate card to clearly explain your pricing structure to users.
- **Cost Descriptions:** Provide clear descriptions for each cost item to help users understand charges and how they connect to your pricing structure.
- **Error Handling:** Always handle `InsufficientFundError` gracefully to provide a good user experience.
- **Minimize Authorizations and Captures:** Use as few calls to authorize and capture as needed for the bot to work well. Each additional call adds complexity and potential friction for users.

## Limitations

- This Monetization API is currently in beta. Please send feedback to developers@poe.com.
- Monetary amounts are specified in milli-cents (thousandths of a cent).
- Bots can only authorize and capture their own costs, not costs for dependency bots called through the Poe Bot API.

---

*This documentation is based on the official Poe Bot Monetization API guide and example code.*
