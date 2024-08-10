/* global $ */

$(document).ready(function () {
  const selectedStates = {};
  const selectedCities = {};

  $('input[type="checkbox"]').change(function () {
    const id = $(this).data('id');
    const name = $(this).data('name');
    if ($(this).is(':checked')) {
      if ($(this).closest('li').parent().parent().is('li')) {
        selectedCities[id] = name;
      } else {
        selectedStates[id] = name;
      }
    } else {
      if ($(this).closest('li').parent().parent().is('li')) {
        delete selectedCities[id];
      } else {
        delete selectedStates[id];
      }
    }
    updateLocations();
  });

  function updateLocations () {
    const locations = Object.values(selectedStates).concat(Object.values(selectedCities));
    $('div.locations h4').text(locations.join(', '));
  }

  $.get('http://0.0.0.0:5001/api/v1/status/', function (data) {
    if (data.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });

  function fetchPlaces (data) {
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function (data) {
        $('section.places').empty();
        for (const place of data) {
          const article = $('<article></article>');
          const titleBox = $('<div class="title_box"></div>');
          titleBox.append(`<h2>${place.name}</h2>`);
          titleBox.append(`<div class="price_by_night">$${place.price_by_night}</div>`);
          article.append(titleBox);

          const information = $('<div class="information"></div>');
          information.append(`<div class="max_guest">${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</div>`);
          information.append(`<div class="number_rooms">${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>`);
          information.append(`<div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>`);
          article.append(information);

          const user = $('<div class="user"></div>');
          user.append(`<b>Owner:</b> ${place.user.first_name} ${place.user.last_name}`);
          article.append(user);

          const description = $('<div class="description"></div>');
          description.html(place.description);
          article.append(description);

          const reviews = $('<div class="reviews" style="margin-top: 40px;"></div>');
          reviews.append(`<h2 style="font-size: 16px; border-bottom: 1px solid #DDDDDD;">Reviews <span class="toggle-reviews" data-place-id="${place.id}">show</span></h2>`);
          reviews.append('<ul class="review-list" style="list-style: none;"></ul>');
          article.append(reviews);

          $('section.places').append(article);
        }
      }
    });
  }

  fetchPlaces({});

  $('button').click(function () {
    const amenities = [];
    $('input[type="checkbox"]:checked').each(function () {
      amenities.push($(this).data('id'));
    });
    fetchPlaces({ amenities, states: Object.keys(selectedStates), cities: Object.keys(selectedCities) });
  });

  $(document).on('click', '.toggle-reviews', function () {
    const span = $(this);
    const placeId = span.data('place-id');
    const reviewList = span.closest('.reviews').find('.review-list');

    if (span.text() === 'show') {
      $.get(`http://0.0.0.0:5001/api/v1/places/${placeId}/reviews`, function (data) {
        reviewList.empty();
        for (const review of data) {
          const reviewItem = $('<li></li>');
          reviewItem.append(`<h3 style="font-size: 14px;">From ${review.user.first_name} ${review.user.last_name} the ${new Date(review.created_at).toLocaleDateString()}</h3>`);
          reviewItem.append(`<p style="font-size: 12px;">${review.text}</p>`);
          reviewList.append(reviewItem);
        }
        span.text('hide');
      });
    } else {
      reviewList.empty();
      span.text('show');
    }
  });
});
