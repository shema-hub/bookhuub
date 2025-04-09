# bookhuub
 Django-library api


✅ Summary Table
Action	Endpoint	Method	Auth?
Register user	/api/users/register/	POST	❌ No
Login (JWT)	/api/users/token/	POST	❌ No
List books	/api/library/books/	GET	❌ No
Add/edit/delete books	/api/library/books/	POST/PUT/DELETE	✅ Admin only
Search books	/api/library/books/?search=	GET	❌ No
Filter available books	/api/library/books/?available=true	GET	❌ No
Checkout book	/api/library/checkout/	POST	✅ Member
Return book	/api/library/return/	POST	✅ Member
Borrow history	/api/library/transactions/	GET	✅ Member