(function () {

    // Handle adding new category
    document.querySelector('#categoryInput').addEventListener('keydown', function (e) {
        if (e.keyCode != 13) {
            return;
        }

        var categoryName = this.value
        this.value = ''
        addNewCategory(categoryName)
        updateCategoriesString()
    })

    function addNewCategory(name) {
        document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend',
            `<li class="category">
        <span class="name">${name}</span>
        <span onclick="removeCategory(this)" class="btnRemove bold">X</span>
      </li>`)
    }

    // Handle removing category
    function removeCategory(e) {
        e.parentElement.remove()
        updateCategoriesString()
    }

    // Fetch category array from HTML
    function fetchCategoryArray() {
        var categories = []
        document.querySelectorAll('.category').forEach(function (e) {
            let name = e.querySelector('.name').innerHTML
            if (name == '') return;
            categories.push(name)
        })
        return categories
    }

    // Update hidden input with category string
    function updateCategoriesString() {
        categories = fetchCategoryArray()
        document.querySelector('input[name="categoriesString"]').value = categories.join(',')
    }

    // Handle auto-updating amount
    document.querySelector('#auto_update').addEventListener('change', function () {
        var start_date = document.querySelector('#start_date').value
        var end_date = document.querySelector('#end_date').value
        var frequency = document.querySelector('#frequency').value
        var amount = document.querySelector('#amount').value
        var auto_update = this.checked

        if (!auto_update) {
            return;
        }

        if (!start_date || !frequency || !amount) {
            alert('Please enter a start date, frequency, and amount before enabling auto update.')
            this.checked = false
            return;
        }

        // Calculate new amount based on frequency
        var diff = moment(end_date).diff(moment(start_date), frequency.toLowerCase())
        var new_amount = amount * (diff + 1)

        document.querySelector('#amount').value = new_amount.toFixed(2)
    })

})();
