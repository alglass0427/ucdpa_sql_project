class Modal extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.isOpen = false;
    this.shadowRoot.innerHTML = `
        <style>
            #backdrop {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100vh;
                background: rgba(0,0,0,0.75);
                z-index: 10;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease-out;
            }

            :host([opened]) #backdrop,
            :host([opened]) #modal {
                opacity: 1;
                pointer-events: all;
            }

            :host([opened]) #modal {
                top: 5vh;
            }

            #modal {
                position: fixed;
                top: 5vh;
                left: 50%;
                transform: translateX(-50%);
                width: 90%;
                max-width: 800px;
                background: white;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.26);
                z-index: 100;
                opacity: 0;
                pointer-events: none;
                transition: all 0.3s ease-out;
            }

            header {
                padding: 1rem;
                border-bottom: 1px solid #ccc;
            }

            #actions {
                border-top: 1px solid #ccc;
                padding: 1rem;
                display: flex;
                justify-content: flex-end;
            }

            #actions button {
                margin: 0 0.25rem;
            }
        </style>
        <div id="backdrop"></div>
        <div id="modal">
            <header>
                <slot name="title">PERFORMANCE</slot>
            </header>
            <section id="main">
                <slot></slot>
            </section>
            <section id="actions">
                <button id="cancel-btn">Cancel</button>
                <button id="confirm-btn">Confirm</button>
            </section>
        </div>
    `;

    const backdrop = this.shadowRoot.querySelector('#backdrop');
    const cancelButton = this.shadowRoot.querySelector('#cancel-btn');
    const confirmButton = this.shadowRoot.querySelector('#confirm-btn');
    
    backdrop.addEventListener('click', this._cancel.bind(this));
    cancelButton.addEventListener('click', this._cancel.bind(this));
    confirmButton.addEventListener('click', this._confirm.bind(this));
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'opened') {
      this.isOpen = this.hasAttribute('opened');
    }
  }

  static get observedAttributes() {
    return ['opened'];
  }

  open() {
    this.setAttribute('opened', '');
  }

  hide() {
    this.removeAttribute('opened');
  }

  _cancel(event) {
    this.hide();
    const cancelEvent = new Event('cancel', { bubbles: true, composed: true });
    this.dispatchEvent(cancelEvent);
  }

  _confirm(event) {
    this.hide();
    const confirmEvent = new Event('confirm', { bubbles: true, composed: true });
    this.dispatchEvent(confirmEvent);
  }
}

customElements.define('uc-modal', Modal);
