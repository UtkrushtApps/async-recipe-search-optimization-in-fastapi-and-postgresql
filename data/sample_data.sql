-- Insert sample categories
INSERT INTO categories (name) VALUES ('Vegan'), ('Dessert'), ('Main Course'), ('Appetizer');
-- Insert sample ingredients
INSERT INTO ingredients (name) VALUES ('Salt'), ('Sugar'), ('Flour'), ('Egg'), ('Milk'), ('Tomato'), ('Garlic'), ('Basil'), ('Chicken'), ('Beef');
-- Insert recipes (about 20 examples, but should be easily extendable)
INSERT INTO recipes (name, category_id, instructions) VALUES ('Vegan Pancakes', 1, 'Mix flour, milk, and baking powder.'), ('Chocolate Cake', 2, 'Mix flour, sugar, eggs, and cocoa, bake.'), ('Chicken Curry', 3, 'Cook chicken with tomato and spices.'), ('Bruschetta', 4, 'Toast bread, add tomato, basil, garlic.');
-- Insert recipe_ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES
(1,3),(1,5),(1,1), -- Vegan Pancakes: Flour, Milk, Salt
(2,3),(2,2),(2,4), -- Chocolate Cake: Flour, Sugar, Egg
(3,9),(3,6),(3,7), -- Chicken Curry: Chicken, Tomato, Garlic
(4,6),(4,8),(4,7); -- Bruschetta: Tomato, Basil, Garlic
-- Insert many more random recipes/ingredients for substantial data
DO $$
DECLARE
  rid INT;
  iid1 INT;
  iid2 INT;
BEGIN
  FOR rid IN 5..50 LOOP
    INSERT INTO recipes (name, category_id, instructions) VALUES ('Recipe ' || rid, ((rid-1)%4)+1, 'Instructions for recipe ' || rid) RETURNING id INTO rid;
    iid1 := ((rid*2-1)%10)+1;
    iid2 := ((rid*3-4)%10)+1;
    INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (rid, iid1);
    INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (rid, iid2);
  END LOOP;
END$$;
