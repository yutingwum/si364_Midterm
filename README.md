# Functionality
- user can enter their name and the application will show names that have visited the site
- user can search for a product using keyword and entering number of item queries they want
- user can add products to their list by entering their username and product id
- user can see all the products in their list by entering their username 

## Functions
- home: allow user to enter their name, provide navigation to links that have other functionalities
- all_names: show names that have visited the site
- search: shows a search form that allow user to search for a product
- search_result: send request to Walmart API using the product keyword and number of search queries that the user enters in the form, and display product search results
- add_product: show a form that asks for username and product id, upon entering, save the useranme and sendd a request to Walmart API with the product id to get the product name; create a user object and a product object and then check if the user and product is in databse. If user is not in databse yet, add it to the databse. If the product is in database already, flash message telling the user the product already exists and redirect to the form. If product does not exist, then add the product to database.
- get_user: show a form that asks for username
- show_products: get username from the form data, find the user object from the database; then make queries to get the user's products from the product table using the user id; finally, display the products


## Models
- Name (id, name)
- User (id, username, and has a one-to-many relationship with Product)
- Prdocut (product_id, user_id, product_name)

## Templates
- 404.html
- base.html (for home)
- name_example.html (for all names)
- search.html (for search)
- product_search_results.html (for search_results)
- add_product.html (for add_product)
- get_user.html (for get_user)
- show_products.html (for show_products)



# Partial checklist of the tasks for instructors

- Include at least 2 additional template .html files we did not provide. Jinja template for loop: ; Jinja template conditional: 


- At least one additional (not provided) WTForm that sends data with a GET request to a new page. (get_user function)
- At least one additional (not provided) WTForm that sends data with a POST request to the same page. (add_product function)
- At least one custom validator for a field in a WTForm. (In Searchform, num_entries has a custom validator)
- At least 2 additional model classes. (User, Product)
- Have a one:many relationship that works properly built between 2 of your models. ((User - Product))
- Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for). (show_products function)
- Query data using an .all() method in at least one view function and send the results of that query to a template. (show_products function, show_products.html) 