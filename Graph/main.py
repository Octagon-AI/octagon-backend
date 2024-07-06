from subgrounds import Subgrounds

# Initialize Subgrounds
sg = Subgrounds()

# Load the Uniswap V2 subgraph
uniswap_v3 = sg.load_subgraph(
    "https://gateway-arbitrum.network.thegraph.com/api/fc92f2b64d2e69e368d79f9892594299/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"
)


ETH_USDC_POOL_1 = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
# ETH_USDC_POOL_2 = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8"

ETH_USDT_POOL_1 = "0x11b815efb8f581194ae79006d24e0d814b7697f6"
# ETH_USDT_POOL_2 = "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36"

ETH_WBTC_POOL = "0x4585fe77225b41b697c938b018e2ac67ac5a20c0"

POOL_IDS = [
    ETH_USDC_POOL_1,
    ETH_USDT_POOL_1,
    ETH_WBTC_POOL,
]
POOL_NAMES = ["ETH_USDC_1", "ETH_USDT_1", "ETH_WBTC"]

DURATION_DAYS = 10

for pool_id, pool_name in zip(POOL_IDS, POOL_NAMES):
    pool_query = uniswap_v3.Query.pools(
        where={"id": "0x11b815efb8f581194ae79006d24e0d814b7697f6"},
    )

    pool_day_data = pool_query.poolDayData(first=DURATION_DAYS)

    day_query_result = sg.query_df(
        [
            pool_query.id,
            pool_query.feeTier,
            pool_day_data.feesUSD,
            pool_day_data.date,
            pool_day_data.liquidity,
            pool_day_data.sqrtPrice,
            pool_day_data.token0Price,
            pool_day_data.token1Price,
            pool_day_data.feeGrowthGlobal0X128,
            pool_day_data.feeGrowthGlobal1X128,
            # pool_day_data.tvlUSD,
            pool_day_data.volumeToken0,
            pool_day_data.volumeToken1,
            pool_day_data.volumeUSD,
            pool_day_data.txCount,
            pool_day_data.open,
            pool_day_data.high,
            pool_day_data.low,
            pool_day_data.close,
        ]
    )

    # print(pool_name)
    print(day_query_result["pools_poolDayData_feesUSD"])
    print(day_query_result["pools_poolDayData_high"])
    print(day_query_result["pools_poolDayData_low"])
    print("\n====================\n")

    # # MSE = |high-P_high| + |low-P_low| + |fee - P_fee|
