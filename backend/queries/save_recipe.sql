INSERT INTO recipes (id, name, Calories, FatContent, SaturatedFatContent, CholesterolContent, SodiumContent,
        CarbohydrateContent, FiberContent, SugarContent, ProteinContent)
        SELECT * FROM (
            SELECT ? AS recipe_id, ? AS name, ? AS Calories, ? AS FatContent, ? AS SaturatedFatContent, ? AS CholesterolContent,
            ? AS SodiumContent, ? AS CarbohydrateContent, ? AS FiberContent, ? AS SugarContent, ? AS ProteinContent
        ) AS tmp
        WHERE NOT EXISTS (
            SELECT 1 FROM recipes WHERE recipe_id = ?
        ) LIMIT 1;