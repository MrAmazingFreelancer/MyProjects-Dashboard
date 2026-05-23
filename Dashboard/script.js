const cards = document.getElementById('cards');
const projectCount = document.getElementById('projectCount');
const addCardButton = document.getElementById('addCardButton');

function updateCount() {
  const count = cards ? cards.children.length : 0;
  if (projectCount) {
    projectCount.textContent = `${count} items`;
  }
}

if (addCardButton && cards) {
  addCardButton.addEventListener('click', () => {
    const article = document.createElement('article');
    article.className = 'card';
    article.innerHTML = `
      <h3>New Demo Card</h3>
      <p>You can replace this with a real project summary.</p>
      <a href="./index.html">Edit this card</a>
    `;

    cards.appendChild(article);
    updateCount();
  });
}

updateCount();
