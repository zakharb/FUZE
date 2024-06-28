class VTopCategories extends HTMLElement {
  constructor() {
    super();
    this.data_url = "";
    this.data_title = "";
    this.data_color = "";
  }

  connectedCallback() {
    this.data_url = this.getAttribute("data_url");
    this.data_title = this.getAttribute("data_title");
    this.data_color = this.getAttribute("data_color");
    this.render();
  }

  async render() {
    this.innerHTML = `
      <div class="vcard chart">
        <div class="vcard-header">
          <div class="vcard-title">
            ${this.data_title}
          </div>
        </div>
        <div class="vcard-body">
          <div class="your-list-container"></div>
        </div>
      </div>
    `;
    await this.loadData();
    this.initScrolling();
  }

  async loadData() {
    const categoriesData = await fetch(this.data_url).then((response) => response.json());
    const listContainer = this.querySelector('.your-list-container');

    listContainer.innerHTML = `
      <ul>
        ${categoriesData.map(({ id, title, count, percent, href }) => `
          <li class="d-none" style="margin: 1em;">
            <a href="${href}" target="_blank">
              <div class="top-title">
                ${title} <span>${count}</span>
              </div>
              <div class="progress progress-xs">
                <div 
                  class="progress-bar" 
                  role="progressbar" 
                  style="width: ${percent}%; background-color: ${this.data_color}">
                </div>
              </div>
            </a>
          </li>
        `).join('')}
      </ul>
    `;
  }
  

  
  initScrolling() {
    const listContainer = this.querySelector('.your-list-container').querySelector('ul');
    const listItems = Array.from(listContainer.querySelectorAll('li'));
    const listLength = listItems.length;
    let scrollingInterval;
  
    const stopScrolling = () => {
      clearInterval(scrollingInterval);
    };
  
    const restartScrolling = () => {
      scrollingInterval = setInterval(() => {
        listItems[7].classList.remove('d-none');
        listItems[0].classList.add('d-none');
        let removedElement = listItems.shift();
        listItems.push(removedElement);
        listContainer.appendChild(removedElement);
      }, 2000);
    };
  
    if (listLength > 7) {
      for (let i = 0; i <= 6; i++) {
        listItems[i].classList.remove('d-none');
      }
  
      restartScrolling();
  
      listContainer.addEventListener('mouseover', stopScrolling);
      listContainer.addEventListener('mouseout', restartScrolling);
    } else {
      listItems.forEach((e) => {
        e.classList.remove('d-none');
      });
    }
  }
  
}

customElements.define("v-top-categories", VTopCategories);
