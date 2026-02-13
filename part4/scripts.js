document.addEventListener("DOMContentLoaded", function () {

  /* =========================
     AUTH UTILITIES
  ========================== */
  
  function getToken() {
    return localStorage.getItem('token');
  }

  function saveToken(token) {
    localStorage.setItem('token', token);
  }

  function removeToken() {
    localStorage.removeItem('token');
  }

  function isLoggedIn() {
    return getToken() !== null;
  }

  function logout() {
    removeToken();
    window.location.href = 'login.html';
  }

  function updateAuthButton() {
    const loginLink = document.querySelector('a[href="login.html"]');
    
    if (loginLink) {
      if (isLoggedIn()) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
          e.preventDefault();
          logout();
        });
      } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
      }
    }
  }

  updateAuthButton();

  /* =========================
     API CONFIGURATION
  ========================== */
  const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

  /* =========================
     API FUNCTIONS
  ========================== */
  
  async function fetchPlaces() {
    try {
      const token = getToken();
      const headers = { 'Content-Type': 'application/json' };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/places/`, {
        method: 'GET',
        headers: headers
      });

      if (response.ok) {
        return await response.json();
      } else if (response.status === 401) {
        removeToken();
        window.location.href = 'login.html';
        return [];
      } else {
        console.error('Failed to fetch places:', response.status);
        return [];
      }
    } catch (error) {
      console.error('Error fetching places:', error);
      return [];
    }
  }

  async function fetchPlaceDetails(id) {
    try {
      const token = getToken();
      const headers = { 'Content-Type': 'application/json' };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/places/${id}`, {
        method: 'GET',
        headers: headers
      });

      if (response.ok) {
        return await response.json();
      } else {
        console.error('Failed to fetch place details:', response.status);
        return null;
      }
    } catch (error) {
      console.error('Error fetching place details:', error);
      return null;
    }
  }

  /* =========================
     HELPER FUNCTIONS
  ========================== */
  let reviews = JSON.parse(localStorage.getItem("reviews")) || [];

  function saveReviews() {
    localStorage.setItem("reviews", JSON.stringify(reviews));
  }

  function generateStars(rating) {
    return "★".repeat(rating) + "☆".repeat(5 - rating);
  }

  /* =========================
     INDEX PAGE LOGIC
  ========================== */
  const placesList = document.getElementById("places-list");
  const priceFilter = document.getElementById("price-filter");

  if (placesList && priceFilter) {
    function populatePriceFilter() {
      priceFilter.innerHTML = '';

      const options = [
        { value: '', text: 'All' },
        { value: '10', text: '$10' },
        { value: '50', text: '$50' },
        { value: '100', text: '$100' }
      ];

      options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.text;
        priceFilter.appendChild(option);
      });
    }

    function displayPlaces(places) {
      placesList.innerHTML = "";

      if (places.length === 0) {
        const noPlaces = document.createElement("p");
        noPlaces.textContent = "No places available.";
        noPlaces.style.textAlign = "center";
        noPlaces.style.color = "#666";
        placesList.appendChild(noPlaces);
        return;
      }

      places.forEach(place => {
        const card = document.createElement("article");
        card.classList.add("place-card");
        card.dataset.price = place.price;
        
        card.innerHTML = `
          <h2>${place.title}</h2>
          <p><strong>Price:</strong> $${place.price} per night</p>
          <p class="description">${place.description || 'No description available'}</p>
          <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        placesList.appendChild(card);
      });
    }

    function filterPlacesByPrice(maxPrice) {
      const cards = placesList.querySelectorAll('.place-card');
      
      cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        
        if (maxPrice === '' || price <= parseFloat(maxPrice)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    }

    priceFilter.addEventListener("change", function () {
      filterPlacesByPrice(this.value);
    });

    async function initializePlacesPage() {
      populatePriceFilter();
      placesList.innerHTML = '<p style="text-align: center;">Loading places...</p>';
      const allPlaces = await fetchPlaces();
      displayPlaces(allPlaces);
    }

    initializePlacesPage();
  }

  /* =========================
     PLACE DETAILS PAGE LOGIC
  ========================== */
  const placeDetailsSection = document.getElementById("place-details");
  const addReviewSection = document.getElementById("add-review");

  if (placeDetailsSection) {
    function getPlaceIdFromURL() {
      const params = new URLSearchParams(window.location.search);
      return params.get("id");
    }

    const placeId = getPlaceIdFromURL();

    async function fetchPlaceReviews(placeId) {
      try {
        const token = getToken();
        const headers = { 'Content-Type': 'application/json' };

        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
          method: 'GET',
          headers: headers
        });

        if (response.ok) {
          return await response.json();
        } else {
          return reviews.filter(r => r.placeId === placeId);
        }
      } catch (error) {
        console.error('Error fetching reviews:', error);
        return reviews.filter(r => r.placeId === placeId);
      }
    }

    async function displayPlaceReviews(placeId) {
      const reviewsSection = document.getElementById("reviews");
      
      if (!reviewsSection) return;

      reviewsSection.innerHTML = "<h2>Reviews</h2><p>Loading reviews...</p>";

      const placeReviews = await fetchPlaceReviews(placeId);

      reviewsSection.innerHTML = "<h2>Reviews</h2>";

      if (placeReviews.length === 0) {
        const p = document.createElement("p");
        p.textContent = "No reviews yet. Be the first to review!";
        p.style.fontStyle = "italic";
        p.style.color = "#666";
        reviewsSection.appendChild(p);
        return;
      }

      placeReviews.forEach(review => {
        const reviewCard = document.createElement("article");
        reviewCard.classList.add("review-card");
        const displayUser = review.user || (review.user_id ? `User ${review.user_id.substring(0, 8)}` : 'Anonymous');
        reviewCard.innerHTML = `
          <p class="review-text">"${review.text}"</p>
          <p><strong>${displayUser}</strong></p>
          <p class="review-rating">${generateStars(review.rating)}</p>
        `;
        reviewsSection.appendChild(reviewCard);
      });
    }

    function displayPlaceDetails(place) {
      placeDetailsSection.innerHTML = "";

      const placeTitle = document.createElement("h1");
      placeTitle.textContent = place.title;
      placeDetailsSection.appendChild(placeTitle);

      const placeInfo = document.createElement("div");
      placeInfo.classList.add("place-info");

      const priceP = document.createElement("p");
      priceP.innerHTML = `<strong>Price:</strong> $${place.price} per night`;
      placeInfo.appendChild(priceP);

      if (place.description) {
        const descP = document.createElement("p");
        descP.innerHTML = `<strong>Description:</strong> ${place.description}`;
        placeInfo.appendChild(descP);
      }

      const locationP = document.createElement("p");
      locationP.innerHTML = `<strong>Location:</strong> Latitude ${place.latitude}, Longitude ${place.longitude}`;
      placeInfo.appendChild(locationP);

      if (place.amenities && place.amenities.length > 0) {
        const amenitiesP = document.createElement("p");
        const amenitiesList = place.amenities.map(a => a.name || a).join(", ");
        amenitiesP.innerHTML = `<strong>Amenities:</strong> ${amenitiesList}`;
        placeInfo.appendChild(amenitiesP);
      }

      placeDetailsSection.appendChild(placeInfo);
    }

    function checkAuthentication() {
      const token = getToken();

      if (!token) {
        if (addReviewSection) {
          addReviewSection.innerHTML = `
            <p style="text-align: center; color: #666;">
              <a href="login.html" class="details-button">Login to add a review</a>
            </p>
          `;
        }
      } else {
        if (addReviewSection) {
          const form = document.createElement("form");
          form.classList.add("form", "add-review");
          form.innerHTML = `
            <h2>Add a Review</h2>
            <label for="review-text">Your Review:</label>
            <textarea id="review-text" rows="4" required placeholder="Share your experience..."></textarea>
            
            <label for="rating">Rating (1-5):</label>
            <input type="number" id="rating" min="1" max="5" required>
            
            <button type="submit">Submit Review</button>
          `;
          
          addReviewSection.innerHTML = "";
          addReviewSection.appendChild(form);

          form.addEventListener("submit", async function (e) {
            e.preventDefault();
            
            const text = document.getElementById("review-text").value.trim();
            const rating = parseInt(document.getElementById("rating").value);
            
            if (!text || !rating) {
              alert("Please fill in all fields.");
              return;
            }

            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';

            try {
              const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ text, rating })
              });

              if (response.ok) {
                alert("Review submitted successfully!");
                
                reviews.push({ placeId, user: "Current User", text, rating });
                saveReviews();
                
                form.reset();
                await displayPlaceReviews(placeId);
              } else {
                const errorData = await response.json().catch(() => ({}));
                alert(errorData.error || 'Failed to submit review. Please try again.');
              }
            } catch (error) {
              console.error('Error submitting review:', error);
              alert('Unable to submit review. Please check your connection.');
            } finally {
              submitButton.disabled = false;
              submitButton.textContent = originalText;
            }
          });
        }
      }
    }

    async function initializePlaceDetailsPage() {
      if (!placeId) {
        placeDetailsSection.innerHTML = '<p>Place not found. Invalid place ID.</p>';
        return;
      }

      placeDetailsSection.innerHTML = '<p>Loading place details...</p>';

      const place = await fetchPlaceDetails(placeId);

      if (place) {
        displayPlaceDetails(place);
        await displayPlaceReviews(placeId);
        checkAuthentication();
      } else {
        placeDetailsSection.innerHTML = '<p>Place not found.</p>';
      }
    }

    initializePlaceDetailsPage();
  }

  /* =========================
     ADD REVIEW PAGE LOGIC
  ========================== */
  const reviewFormPage = document.getElementById("review-form");
  const placeNameElement = document.getElementById("place-name");

  if (reviewFormPage) {
    function checkAuthentication() {
      const token = getToken();
      if (!token) {
        window.location.href = 'index.html';
        return null;
      }
      return token;
    }

    function getPlaceIdFromURL() {
      const params = new URLSearchParams(window.location.search);
      return params.get("id");
    }

    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!token) return;

    if (!placeId) {
      alert('Invalid place ID');
      window.location.href = 'index.html';
      return;
    }

    async function initializeReviewForm() {
      const place = await fetchPlaceDetails(placeId);
      
      if (place && placeNameElement) {
        placeNameElement.textContent = `Reviewing: ${place.title}`;
      } else if (placeNameElement) {
        placeNameElement.textContent = 'Add Your Review';
      }
    }

    initializeReviewForm();

    const starContainer = document.getElementById("star-rating");
    const ratingInput = document.getElementById("rating");
    let selectedRating = 0;

    if (starContainer && ratingInput) {
      const stars = starContainer.querySelectorAll("span");

      stars.forEach(star => {
        star.addEventListener("mouseenter", () => {
          const val = parseInt(star.dataset.value);
          stars.forEach(s => s.classList.toggle("hovered", parseInt(s.dataset.value) <= val));
        });

        star.addEventListener("mouseleave", () => {
          stars.forEach(s => s.classList.remove("hovered"));
        });

        star.addEventListener("click", () => {
          selectedRating = parseInt(star.dataset.value);
          ratingInput.value = selectedRating;
          stars.forEach(s => s.classList.toggle("selected", parseInt(s.dataset.value) <= selectedRating));
        });
      });
    }

    async function submitReview(token, placeId, reviewText, rating) {
      try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ text: reviewText, rating })
        });

        return response;
      } catch (error) {
        console.error('Error submitting review:', error);
        throw error;
      }
    }

    reviewFormPage.addEventListener("submit", async function (e) {
      e.preventDefault();
      
      const reviewText = document.getElementById("review").value.trim();
      const rating = parseInt(document.getElementById("rating").value);

      if (!reviewText) {
        alert("Please write a review.");
        return;
      }

      if (!rating || rating < 1 || rating > 5) {
        alert("Please select a rating between 1 and 5.");
        return;
      }

      const submitButton = reviewFormPage.querySelector('button[type="submit"]');
      const originalButtonText = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = 'Submitting...';

      try {
        const response = await submitReview(token, placeId, reviewText, rating);

        if (response.ok) {
          alert('Review submitted successfully!');
          
          reviews.push({ placeId, user: "Current User", text: reviewText, rating });
          saveReviews();
          
          window.location.href = `place.html?id=${placeId}`;
        } else {
          const errorData = await response.json().catch(() => ({}));
          const errorMessage = errorData.error || 'Failed to submit review. Please try again.';
          alert(errorMessage);
          
          submitButton.disabled = false;
          submitButton.textContent = originalButtonText;
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Unable to submit review. Please check your connection and try again.');
        
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
      }
    });
  }

  /* =========================
     LOGIN PAGE LOGIC
  ========================== */
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const errorMessageEl = document.getElementById('error-message');
      const submitButton = loginForm.querySelector('button[type="submit"]');

      if (errorMessageEl) {
        errorMessageEl.textContent = '';
      }

      const originalButtonText = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = 'Logging in...';

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          saveToken(data.access_token);
          submitButton.textContent = 'Success! Redirecting...';
          setTimeout(() => {
            window.location.href = 'index.html';
          }, 500);
        } else {
          let errorMessage = '';

          if (response.status === 401) {
            errorMessage = '❌ Invalid email or password. Please check your credentials and try again.';
          } else if (response.status === 400) {
            errorMessage = '❌ Please provide both email and password.';
          } else if (response.status === 500) {
            errorMessage = '❌ Server error. Please try again later.';
          } else if (response.status === 404) {
            errorMessage = '❌ Account not found. Please check your email address.';
          } else {
            try {
              const errorData = await response.json();
              errorMessage = `❌ ${errorData.error || 'Login failed. Please try again.'}`;
            } catch {
              errorMessage = '❌ Login failed. Please try again.';
            }
          }

          if (errorMessageEl) {
            errorMessageEl.textContent = errorMessage;
          }

          submitButton.disabled = false;
          submitButton.textContent = originalButtonText;
        }
      } catch (error) {
        console.error('Login error:', error);
        
        if (errorMessageEl) {
          errorMessageEl.textContent = '❌ Unable to connect to the server. Please check your internet connection and try again.';
        }

        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
      }
    });
  }

});