# Ecommerce Full-Stack Project (Django)

A responsive eCommerce storefront built with Django + Bootstrap 5, with a
Django REST Framework + JWT API layer for CRUD operations.

## Stack
- **Frontend:** Django templates, Bootstrap 5 (12-column grid, Flexbox)
- **Backend:** Django 5/6, Django REST Framework
- **Auth:** Django session auth (storefront pages) + JWT via `djangorestframework-simplejwt` (API)
- **Database:** SQLite (default, zero-config)
- **Admin panel:** Django's built-in `/admin/` (protected, staff-only)

## 1. Setup (first time)

```bash
# from the project root (where manage.py lives)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

# create an admin/superuser account (for /admin/ and admin-only API actions)
python manage.py createsuperuser

# load sample products into the database
python manage.py seed_products

python manage.py runserver
```

Visit:
- Storefront: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- API root: http://127.0.0.1:8000/api/products/

## 2. Project structure

```
ecommerce/
├── core_app/        # Home page
├── products_app/    # Product model, listing/grid/detail pages, DRF API
├── cart_app/        # Cart model, cart page, add/remove/update actions
├── accounts_app/    # Login/signup pages + JWT register/login API
├── templates/        
├── static/          # CSS, images
└── media/           # Uploaded product images (created on first seed/upload)
```

## 3. REST API (CRUD + JWT)

| Method | Endpoint                     | Auth required   | Description                  |
|--------|-------------------------------|-----------------|-------------------------------|
| GET    | `/api/products/`              | No              | List products (search/filter) |
| GET    | `/api/products/<id>/`         | No              | Retrieve one product          |
| POST   | `/api/products/`               | Staff JWT       | Create product                |
| PUT    | `/api/products/<id>/`         | Staff JWT       | Update product                |
| DELETE | `/api/products/<id>/`         | Staff JWT       | Delete product                |
| POST   | `/api/auth/register/`          | No              | Register + receive JWT tokens |
| POST   | `/api/auth/login/`             | No              | Obtain JWT access/refresh     |
| POST   | `/api/auth/refresh/`           | No              | Refresh JWT access token      |
| GET    | `/api/auth/me/`                | JWT             | Current user info             |

**Search & filter (query params on `/api/products/`):**
- `?search=watch` — free text search across name/description/category
- `?category=electronics`
- `?min_price=10&max_price=100`
- `?ordering=price` or `-price`

**Using JWT from the API:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'

# Response: {"refresh": "...", "access": "..."}

curl -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/auth/me/
```

## 4. Why session auth on the website but JWT on the API?

The storefront is server-rendered (Django templates need `request.user`
directly), so it uses Django's built-in session auth for login/signup/logout.
The JWT endpoints under `/api/auth/` exist to satisfy the token-based auth
requirement and to let any external client (mobile app, Postman, another
frontend) authenticate against the same product/cart data via the API.

## 5. Deployment (Render / Vercel / Heroku)

1. Push to GitHub.
2. Set environment variables on your host:
   - `SECRET_KEY` — any long random string
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — your deployed domain, e.g. `your-app.onrender.com`
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start command: `gunicorn ecommerce.wsgi`
5. After first deploy, run once (via host's shell/console):
   ```bash
   python manage.py createsuperuser
   python manage.py seed_products
   ```

> Note: SQLite works for a demo deployment but resets on Render's free tier
> redeploys since the filesystem isn't persistent. For a more permanent
> deployment, swap to a managed Postgres add-on later — the Django ORM code
> doesn't need to change, only `DATABASES` in `settings.py`.

## 6. Suggested commit history (matches the 3 weekly milestones)

```bash
git add .
git commit -m "Week 1: Static responsive frontend - Home, Listing, Details, Cart pages"

# after backend + dynamic integration
git commit -m "Week 2: Django backend with CRUD API and dynamic frontend integration"

# after auth, cart persistence, admin panel, deploy config
git commit -m "Week 3: JWT auth, cart persistence, admin panel, deployment ready"
```
