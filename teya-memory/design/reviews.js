(function () {
  var root = document.getElementById("otzyvy-list");
  if (!root) return;

  function esc(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function isPublished(item) {
    return item && item.status === "published" && String(item.text || "").trim();
  }

  function authorLabel(item) {
    var name = String(item.author || "").trim();
    if (isPublished(item) && name) return name;
    return "Отзыв будет добавлен";
  }

  function eventLabel(item) {
    var event = String(item.event_type || "").trim();
    if (isPublished(item) && event) return event;
    return "тип события появится с отзывом";
  }

  function dateLabel(item) {
    var date = String(item.date || "").trim();
    if (isPublished(item) && date) return date;
    return "карточка-заглушка";
  }

  function bodyText(item) {
    var text = String(item.text || "").trim();
    if (isPublished(item) && text) return text;
    return "Оригинальный текст, имя и дата появятся здесь. Компанию называем только с согласием. Оценку не выдумываем.";
  }

  function mediaHtml(item) {
    var photo = String(item.photo || "").trim();
    if (isPublished(item) && photo) {
      return '<img src="' + esc(photo) + '" alt="">';
    }
    return '<p class="script">скоро</p>';
  }

  function shotHtml(item) {
    var shot = String(item.screenshot || "").trim();
    if (!(isPublished(item) && shot)) return "";
    return (
      '<a class="review-shot" href="' + esc(shot) + '">' +
        '<img src="' + esc(shot) + '" alt="Скриншот исходного отзыва">' +
      "</a>"
    );
  }

  function cardHtml(item) {
    var published = isPublished(item);
    return (
      '<article class="venue-card' + (published ? "" : " is-placeholder") + '"' +
        (item.id ? ' data-review-id="' + esc(item.id) + '"' : "") + ">" +
        '<div class="venue-card-media" aria-hidden="' + (published && item.photo ? "false" : "true") + '">' +
          mediaHtml(item) +
        "</div>" +
        '<div class="venue-card-body">' +
          '<p class="venue-kicker">' + esc(eventLabel(item)) + "</p>" +
          '<h3 class="venue-name">' + esc(authorLabel(item)) + "</h3>" +
          '<p class="venue-text">' + esc(bodyText(item)) + "</p>" +
          shotHtml(item) +
          '<p class="venue-link">' + esc(dateLabel(item)) + "</p>" +
        "</div>" +
      "</article>"
    );
  }

  function schemaFor(items) {
    var published = items.filter(isPublished);
    if (!published.length) return null;
    return {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "itemListElement": published.map(function (item, index) {
        var review = {
          "@type": "Review",
          "author": { "@type": "Person", "name": authorLabel(item) },
          "reviewBody": String(item.text).trim(),
          "itemReviewed": {
            "@type": "LocalBusiness",
            "@id": "https://dedmoroz52.ru/#organization",
            "name": "Дед Мороз и Снегурочка | Нижний Новгород"
          }
        };
        if (item.date) review.datePublished = String(item.date).trim();
        if (item.rating != null && item.rating !== "") {
          review.reviewRating = {
            "@type": "Rating",
            "ratingValue": String(item.rating),
            "bestRating": "5"
          };
        }
        return {
          "@type": "ListItem",
          "position": index + 1,
          "item": review
        };
      })
    };
  }

  function injectSchema(data) {
    var holder = document.getElementById("review-jsonld");
    if (!holder) return;
    if (!data) {
      holder.textContent = "";
      return;
    }
    holder.setAttribute("type", "application/ld+json");
    holder.textContent = JSON.stringify(data);
  }

  fetch("reviews.json", { cache: "no-store" })
    .then(function (res) { return res.ok ? res.json() : null; })
    .then(function (data) {
      var items = data && Array.isArray(data.reviews) ? data.reviews : [];
      if (!items.length) return;
      root.innerHTML = items.map(cardHtml).join("");
      injectSchema(schemaFor(items));
    })
    .catch(function () {});
})();
