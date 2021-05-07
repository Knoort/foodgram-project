class Api {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
  }
  getPurchases() {
    return fetch(`${this.apiUrl}/purchases/`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addPurchases(id) {
    // debugger
    return fetch(`${this.apiUrl}/purchases/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({
        recipe: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removePurchases(id) {
    // debugger
    console.log('удаление заказа: ', id)
    return fetch(`${this.apiUrl}/purchases/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
      .then(e => {
        if (e.ok) {
          return JSON.stringify(e)
          // return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(`${this.apiUrl}/subscriptions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({
        author: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions(id) {
    return fetch(`${this.apiUrl}/subscriptions/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
      .then(res => {
        if (res.ok) {
          return JSON.stringify(res)
          // return res.json()
        }
        return Promise.reject(res.statusText)
      })
  }
  addFavorites(id) {
    // debugger
    return fetch(`${this.apiUrl}/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        // 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0]
      },
      body: JSON.stringify({
        recipe: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removeFavorites(id) {
    // debugger
    console.log('removeFavorites: ', id)
    return fetch(`${this.apiUrl}/favorites/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
      .then(res => {
        if (res.ok) {
          return JSON.stringify(res) // res.json()
        }
        return Promise.reject(res.statusText)
      })
  }
  getIngredients(text) {
    return fetch(`${this.apiUrl}/ingredients?search=${text}&limit=6`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(e => {
        if (e.ok) {
          // console.log('успешный ответ сервера', e)
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
}
