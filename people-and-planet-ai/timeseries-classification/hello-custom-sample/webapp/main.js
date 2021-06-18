import {html, render} from 'https://unpkg.com/lit-html@1?module';
import {LinearProgress} from 'https://unpkg.com/@material/mwc-linear-progress@0.20?module';
import {CLOUD_FUNCTION_URL} from './function-url.js';

const refreshButton = document.querySelector('button');
const cards = document.querySelectorAll('.mdc-card');

const progressBar = (label) => {
  const bar = new LinearProgress();
  bar.indeterminate = true;
  bar.ariaLabel = label;
  return bar;
};

const cardTemplate = (image, label, loadingOrPrediction = '') =>
  html`<div class="mdc-card__media">${image}</div>
  <h2 class="mdc-typography--headline-5">${label}</h2>
  <button @click=${getPrediction}
      class="mdc-card__primary-action ${loadingOrPrediction ? 'hidden' : ''}"
      aria-label="Get prediction"></button>
  ${loadingOrPrediction}`;

const predictionTemplate = (probabilities) =>
  html`<p>Prediction (probabilities):</p>
  <ul>
    ${probabilities.map((p) => html`<li>${p[0]}: ${p[1]}</li>`)}
  </ul>`;

const showImagesAreLoading = function showImagesAreLoading() {
  refreshButton.setAttribute('disabled', '');
  cards.forEach((card) => {
    render(progressBar('Loading flower photo'), card);
  });
};

const fetchImageList = async function fetchImageList() {
  const res = await fetch('image-list.txt');
  const text = await res.text();
  return text.split('\n');
};

const refreshImages = async function refreshImages(imageList) {
  // Choose 6 images from list
  const choices = new Set();
  while (choices.size < 6) {
    const index = Math.floor(Math.random() * imageList.length);
    choices.add(imageList[index]);
  }

  // Load each image in background, then render it with its label
  const imagesLoaded = Array.from(choices).map((imagePath, i) => {
    const card = cards[i];
    const label = imagePath.split('/')[0];
    const image = new Image();
    image.src = `https://storage.googleapis.com/cloud-ml-data/img/flower_photos/${imagePath}`;
    image.alt = label;
    return new Promise((resolve) => {
      image.onload = () => {
        render(cardTemplate(image, label), card);
        resolve();
      };
      image.onerror = (err) => {
        render(html`This image could not be loaded.`, card);
        resolve();
      };
    });
  });
  await Promise.all(imagesLoaded);
  refreshButton.removeAttribute('disabled');
};

export const getPrediction = async function getPrediction(ev) {
  const card = ev.currentTarget.parentNode;
  const image = card.querySelector('img');
  const label = card.querySelector('h2').textContent;

  // Show prediction is loading
  render(cardTemplate(image, label, progressBar('Getting prediction')), card);

  // Get prediction from Cloud Function
  const res = await fetch(CLOUD_FUNCTION_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({image_url: image.src}),
  });
  if (!res.ok) {
    render(cardTemplate(image, label, 'Error getting prediction'), card);
    return;
  }
  const probabilities = await res.json();

  // If user has refreshed image, don't show result
  if (card.querySelector('img').src !== image.src) return;

  // Render prediction
  render(cardTemplate(image, label, predictionTemplate(probabilities)), card);
};

const main = async function main() {
  // Add progress indicators until image list loads, then add images
  showImagesAreLoading();
  const imageList = await fetchImageList();
  refreshImages(imageList);

  // Set up refreshButton to fetch new images
  refreshButton.onclick = () => {
    showImagesAreLoading();
    refreshImages(imageList);
  };
};

main();
