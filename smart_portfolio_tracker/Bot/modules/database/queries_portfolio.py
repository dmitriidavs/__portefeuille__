SQL_ADD_ASSET_TO_PORTFOLIO = """
INSERT INTO portfolio (
    user_id,
    asset_id,
    quantity
) VALUES (
    {user_id},
    (
        SELECT
            asset_id
        FROM assets
        WHERE ticker_symbol = '{asset_name}'
    ),
    {asset_quantity}
);
"""

SQL_DELETE_PORTFOLIO = """
DELETE FROM portfolio
WHERE user_id = {user_id}
"""

# # pg way
# SQL_DELETE_PORTFOLIO = """
# WITH deleted AS (
#     DELETE FROM portfolio
#     WHERE user_id = {user_id}
#     RETURNING *
# )
# SELECT COUNT(*) FROM deleted;
# """

SQL_SELECT_ASSETS_OUTER = """
SELECT
    ticker_symbol,
    SUM(quantity)
FROM portfolio AS p
INNER JOIN assets AS a
    ON a.asset_id = p.asset_id
WHERE user_id = {user_id}
GROUP BY user_id, p.asset_id;
"""

SQL_SELECT_ASSETS_INNER = """
SELECT
    asset_id,
    quantity,
    added_at
FROM portfolio
WHERE user_id = {user_id} AND asset_id = {asset_id}
ORDER BY added_at;
"""