# Read Me

Brief outline of the implementation for each spec:

1. **Models:** Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
```
I have 4 models established in models.py: User, Listing, Bids, and Comments.
```

2. **Create Listing:** Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
```
Clicking the "Create Listing" link on index.html brings the user to the create_listing.html.  A Django form from forms.py is used to collect info and validate fields.
```

3. **Active Listings Page:** The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
```
Index.html provides a list of ACTIVE listings, their titles, descriptions, bids, and images.
```

4. **Listing Page:** Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
```
Listing links on index.html point to views.listing_page which renders listing_page.html with the listing's data as context.
```

  - If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.

```
Authenticated users are displayed the watch/unwatch button on listing_page.html.  This button toggles between watch & unwatch depending on whether the user is already watching the listing.  This logic is also enforced by the views.watch method.
```

  - If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
```
This information is collected via a django form on listing_page.html.  The views.bid method determines if the bid is >= the starting bid and > any other bids.  If not, views.bid renders listing_page.html with an error message for the user.
```

  - If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
```
This spec is fulfilled by the conditional "close" button on the listing page.  The views.close method enforces the requirement that the authenticated user is the owner of the listing.
```

  - If a user is signed in on a closed listing page, and the user has won that auction, the page should say so. 
```
This spec is fulfilled by the conditional message on listing_page.html.  I also added a "my winning bids" link to the main menu bar to make these listings easier to access (since they no longer appear on "active listings" once they are closed).
```

  - Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.
```
listing_page.html displays a list of comments pertaining to the specific listing.  If the user is authenticated, a form also displays on listing_page.html to collect a comment from the user.
```

5. **Watchlist:** Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
```
The watchlist link in the top menu bar directs authenticated users to the watchlist page (which is simply a conditionally-formatted version of index.html).

PLEASE NOTE: As the spec requires, this list includes closed listings that may be on a user's watchlist in addition to active listings.
```

6. **Categories:** Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
```
The categories link on the top menu bar directs users to a list of all ACTIVE categories at categories.html.  Clicking on any category directs the user to a list of active listings for that category on category_listing.html.  Clicking on any specific listing behaves just as it does from the index page.
```

7. **Django Admin Interface:** Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.
```
All four models - User, Listing, Bids, and Comments - have been registered on admin.py and are fully accessible via the Django admin interface.
```