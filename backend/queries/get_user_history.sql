SELECT id, Calories, FatContent, SaturatedFatContent,
CholesterolContent, SodiumContent, CarbohydrateContent,
FiberContent, SugarContent, ProteinContent
FROM recipes
WHERE id IN (
    SELECT recipe_id FROM user_recipes
    WHERE user_id = (
        SELECT id FROM users
        WHERE name = ?
    )
)