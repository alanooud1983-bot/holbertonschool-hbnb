# API Testing Report

# Users Endpoint

### 1. Create User — POST /api/v1/users/

**Success — Create a new user (201 Created)**

**Request:**
<img width="903" height="435" alt="image" src="https://github.com/user-attachments/assets/7f0d1467-3aca-48c8-ade1-393b676607d4" />

**Error — Duplicate email (400 Bad Request)**

**Request:**
<img width="928" height="319" alt="image" src="https://github.com/user-attachments/assets/f075589b-decc-44d5-a8e1-ad9f97418777" />


**Error — Missing required field (400 Bad Request)**

**Request:**
<img width="921" height="390" alt="image" src="https://github.com/user-attachments/assets/45f84075-9f30-4fe7-baf3-f88dd0e9172e" />

**Error — Invalid email format (400 Bad Request)**

**Request:**
<img width="946" height="349" alt="image" src="https://github.com/user-attachments/assets/9a6aa49d-b0d0-4d75-b5fb-8ba916a64637" />


### 2. Retrieve User by ID — GET /api/v1/users/<user_id>

**Success — User exists (200 OK)**

**Request:**
<img width="922" height="289" alt="image" src="https://github.com/user-attachments/assets/540e2215-17e0-417c-9369-17c1bfb1d3b7" />

**Error — User not found (404 Not Found)**

**Request:**
<img width="927" height="201" alt="image" src="https://github.com/user-attachments/assets/105970e7-5586-4b0b-9077-9816876225fa" />


### 3. Retrieve List of Users — GET /api/v1/users/

**Success — List users (200 OK)**

**Request:**
<img width="907" height="518" alt="image" src="https://github.com/user-attachments/assets/4fe988a2-4a87-4565-bccb-20d0e627449f" />


### 4. Update User — PUT /api/v1/users/<user_id>

**Success — Update all fields (200 OK)**

**Request:**
<img width="913" height="437" alt="image" src="https://github.com/user-attachments/assets/8fddc557-f384-478e-b777-fdc76e9af24c" />

**Error — User not found (404 Not Found)**

**Request:**
<img width="920" height="346" alt="image" src="https://github.com/user-attachments/assets/f03b4389-b9e8-4ed4-9f91-7c759a35d824" />

**Error — Invalid data (400 Bad Request)**

**Request:**
<img width="915" height="288" alt="image" src="https://github.com/user-attachments/assets/4bd735af-fa25-40a2-a2a1-3977efd59941" />

# 2. Amenities Endpoint

### 1. Create Amenity — POST /api/v1/amenities/

**Success — Create a new amenity (201 Created)**

**Request:**

<img width="828" height="219" alt="image" src="https://github.com/user-attachments/assets/24fa2614-1a13-40d4-b905-a751e783371c" />

**Error — Missing name (400 Bad Request)**

**Request:**

<img width="831" height="153" alt="image" src="https://github.com/user-attachments/assets/be2dbc43-556f-4e6d-83a9-5e8ad86008d2" />

**Error — Name Too Long (>50 chars)**

**Request:**

<img width="920" height="338" alt="image" src="https://github.com/user-attachments/assets/334556de-1c8f-48ba-9c3c-f82e9d6a87bd" />

### 2. Retrieve All Amenities — GET /api/v1/amenities/

**Success — Get list of amenities (200 OK)**

**Request:**

<img width="833" height="204" alt="image" src="https://github.com/user-attachments/assets/9be42692-4e7d-4039-826a-b90ee9179f4a" />


### 3. Retrieve Amenity by ID — GET /api/v1/amenities/<amenity_id>

**Success — Amenity exists (200 OK)**

**Request:**

<img width="936" height="179" alt="image" src="https://github.com/user-attachments/assets/ec9f2894-0742-4695-9e35-a930c6f829c4" />

**Error — Amenity not found (404 Not Found)**

**Request:**

<img width="931" height="151" alt="image" src="https://github.com/user-attachments/assets/222b0aa5-1fc3-4d1e-a118-3c8804d37170" />


### 4. Update Amenity — PUT /api/v1/amenities/<amenity_id>

**Success — Update name (200 OK)**

**Request:**

<img width="925" height="235" alt="image" src="https://github.com/user-attachments/assets/0293ec09-b92c-4d71-8ba0-757135d43b80" />

**Error — Amenity not found (404 Not Found)**

**Request:**

<img width="908" height="218" alt="image" src="https://github.com/user-attachments/assets/0899969b-d4ad-4624-9b8e-4c359ccf95d5" />


# 3. Places Endpoint


### 1. Create Place — POST /api/v1/places/

**Success — Create a new place (201 Created)**

**Request:**

<img width="832" height="429" alt="image" src="https://github.com/user-attachments/assets/d17bc77e-83e2-4e01-86f5-1f936d514750" />

**Error — Missing required field (400 Bad Request)**

**Request:**

<img width="809" height="321" alt="image" src="https://github.com/user-attachments/assets/cc16f600-b243-4795-9894-8e95da42f8a1" />

**Error - Invalid Price (≤ 0)**

**Request:**

<img width="932" height="407" alt="image" src="https://github.com/user-attachments/assets/08e61549-28a1-45b4-9e7e-2ac073544cd9" />

**Error - Invalid Latitude**

**Request:**

<img width="940" height="413" alt="image" src="https://github.com/user-attachments/assets/22090d62-61c4-4d8c-8d50-2416f2b0b500" />

**Error - Invalid Longitude**

**Request:**

<img width="918" height="401" alt="image" src="https://github.com/user-attachments/assets/065ff008-f1b4-4be2-9c49-60eeaf3cb7df" />

**Error - Owner Does Not Exist**

**Request:**

<img width="939" height="387" alt="image" src="https://github.com/user-attachments/assets/f495a456-d3bc-47d0-bc5f-d6bc3638021f" />


### 2. Retrieve All Places — GET /api/v1/places/

**Success — List of places (200 OK)**

**Request:**

<img width="813" height="300" alt="image" src="https://github.com/user-attachments/assets/5104b8e1-48fa-42fc-b9ec-9260e82bd7cf" />

### 3. Retrieve Place by ID — GET /api/v1/places/<place_id>

**Success — Place exists (200 OK)**

**Request:**

<img width="939" height="462" alt="image" src="https://github.com/user-attachments/assets/bbf30ba2-6593-4844-b622-89a535e1fae3" />

**Error — Place not found (404 Not Found)**

**Request:**

<img width="941" height="158" alt="image" src="https://github.com/user-attachments/assets/b0ba28bf-af2e-463c-afe5-5862edb9dce8" />

### 4. Update Place — PUT /api/v1/places/<place_id>

**Success — Update fields (200 OK)**

**Request:**

<img width="914" height="553" alt="image" src="https://github.com/user-attachments/assets/1b2a44a9-ea44-4003-85ce-d7da0bf9c993" />

**Error — Place not found (404 Not Found)**

**Request:**

<img width="916" height="240" alt="image" src="https://github.com/user-attachments/assets/e14a8411-4409-41fe-969e-4cd275f7b326" />


# 4. Reviews Endpoint

### 1. Create Review POST /api/v1/reviews/

**Success — Create a new review (201 Created)**

**Request:**

<img width="902" height="480" alt="image" src="https://github.com/user-attachments/assets/ee497c57-8f54-4082-b784-29c8c416b002" />

**Error — Missing required fields (400 Bad Request)**

**Request:**

<img width="915" height="290" alt="image" src="https://github.com/user-attachments/assets/2028dc15-d396-4c3b-bafb-e5ea538842f1" />

**Error — Invalid rating (400 Bad Request)**

**Request:**

<img width="904" height="372" alt="image" src="https://github.com/user-attachments/assets/4c513dec-85f3-4411-bf85-8d1b78b1b2b4" />

### 2. Retrieve All Reviews GET /api/v1/reviews/

**Success — Get all reviews (200 OK)**

**Request:**

<img width="933" height="354" alt="image" src="https://github.com/user-attachments/assets/51c18df3-03b2-4675-b1c8-446290bfae2a" />

### 3. Retrieve Review by ID GET /api/v1/reviews/<review_id>

**Success — Review exists (200 OK)**

**Request:**

<img width="921" height="294" alt="image" src="https://github.com/user-attachments/assets/84b6a1ad-0cbb-4095-9fdc-335bf8866da1" />

**Error — Review not found (404 Not Found)**

**Request:**

<img width="931" height="175" alt="image" src="https://github.com/user-attachments/assets/a8a8995f-a1bd-472d-ab89-0455863efe38" />

### 4. Update Review PUT /api/v1/reviews/<review_id>

**Success — Update review (200 OK)**

**Request:**

<img width="917" height="430" alt="image" src="https://github.com/user-attachments/assets/61cd8d07-7c10-455e-a3e1-3db35afe00bb" />

**Error — Review not found (404 Not Found)**

**Request:**

<img width="940" height="324" alt="image" src="https://github.com/user-attachments/assets/ae99bac1-8ccb-4f41-ac53-320f2aeefccd" />

### 5. Delete Review DELETE /api/v1/reviews/<review_id>

**Success — Delete review (200 OK)**

**Request:**

<img width="927" height="187" alt="image" src="https://github.com/user-attachments/assets/ac883fdd-7947-429f-b5e5-ce06bb667973" />

**Error — Review not found (404 Not Found)**

**Request:**

<img width="919" height="179" alt="image" src="https://github.com/user-attachments/assets/1358cb9e-588d-441e-b63f-5d526285dd91" />

### 6. Retrieve All Reviews for a Place GET /api/v1/places/<place_id>/reviews

**Success — Reviews for place (200 OK)**

**Request:**

<img width="919" height="351" alt="image" src="https://github.com/user-attachments/assets/292dc79d-ea4f-4b2a-a349-7d378d39a6c9" />

**No Reviews**

<img width="909" height="124" alt="image" src="https://github.com/user-attachments/assets/64613f78-8f47-419c-92fd-3a18e5f25495" />

**Error — Place not found (404 Not Found)**

**Request:**

<img width="929" height="176" alt="image" src="https://github.com/user-attachments/assets/c2ea8754-8aca-41ac-9472-1fd08ff53510" />
