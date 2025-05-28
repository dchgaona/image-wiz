# 🧙 Image-Wiz

**Image-Wiz** is a FastAPI-powered image processing and transformation API. It allows users to upload images and apply various transformations, filters, compressions, and watermarks through a clean RESTful interface. Ideal for applications needing real-time image manipulation with user authentication support.

---

## 🚀 Features

- ✅ Upload and retrieve images
- 🧹 Transform: mirror, flip, rotate, resize, crop
- 🎨 Filters: grayscale, sepia, negative, posterize, sharpen
- 🗜️ Format conversion and compression
- 💧 Add text watermarks
- 🔐 User registration and login
- 📘 Auto-generated OpenAPI 3.1 documentation

---

## 📦 Installation

```bash
git clone https://github.com/dchgaona/image-wiz.git
cd image-wiz
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
````

---

## 🛠️ Running the Server

```bash
fastapi dev src/app.py
```

Then visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## 📡 API Overview

### 🖼️ Image Operations

| Method   | Endpoint                 | Description       |
| -------- | ------------------------ | ----------------- |
| `POST`   | `/api/images/upload`     | Upload an image   |
| `GET`    | `/api/images/{image_id}` | Get an image      |
| `DELETE` | `/api/images/{image_id}` | Delete an image   |
| `GET`    | `/api/images`            | Get all images    |
| `DELETE` | `/api/images`            | Delete all images |

### 🔄 Transformations

| Endpoint                           | Description  |
| ---------------------------------- | ------------ |
| `/api/transform/mirror/{image_id}` | Mirror image |
| `/api/transform/flip/{image_id}`   | Flip image   |
| `/api/transform/rotate/{image_id}?degrees={degrees}` | Rotate image |
| `/api/transform/resize/{image_id}?width={w}&height={h}` | Resize image |
| `/api/transform/crop/{image_id}?left={l}&top={t}&right={r}&bottom={b}`   | Crop image   |

### 🎨 Filters

| Endpoint                           | Description |
| ---------------------------------- | ----------- |
| `/api/filter/grayscale/{image_id}` | Grayscale   |
| `/api/filter/negative/{image_id}`  | Negative    |
| `/api/filter/posterize/{image_id}?bits={1-8}` | Posterize   |
| `/api/filter/sepia/{image_id}`     | Sepia       |
| `/api/filter/sharpen/{image_id}`   | Sharpen     |

### ⚙️ Data Handling

| Endpoint                              | Description          |
| ------------------------------------- | -------------------- |
| `/api/data/format/{image_id}?new_format={format}`         | Convert image format |
| `/api/data/compress/{image_id}`       | Compress image       |
| `POST /api/data/watermark/{image_id}` | Add watermark text   |

### 🔐 Authentication

| Method | Endpoint        | Description             |
| ------ | --------------- | ----------------------- |
| `POST` | `/api/register` | Register a new user     |
| `POST` | `/api/login`    | Login and receive token |

---

## 🔐 Authentication

All endpoints are protected and require a Bearer token. Use `/api/login` to obtain one and include it in your headers:

```
Authorization: Bearer <your_token>
```

---

## 🧪 Example Usage

```bash
curl -X POST "http://localhost:8000/api/images/upload" \
  -H "accept: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@example.jpg"
```

---

## 🧰 Built With

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pillow](https://pillow.readthedocs.io/)
* [Uvicorn](https://www.uvicorn.org/)
* [Pydantic](https://pydantic.dev/)

---

## 📝 License

MIT License © [@dchgaona](https://github.com/dchgaona)

---

## 📷 Swagger Preview

You can explore and test the API visually at:

```
http://localhost:8000/docs
```

---
