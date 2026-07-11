const employeeDropdown = document.getElementById("employee");
const employeeName = document.getElementById("employee_name");

function updateEmployeeName(){

    const selected =
        employeeDropdown.options[
            employeeDropdown.selectedIndex
        ];

    employeeName.value =
        selected.dataset.name;

}

employeeDropdown.addEventListener(
    "change",
    updateEmployeeName
);

updateEmployeeName();

employee.addEventListener("change", function () {
    const selectedOption = employee.options[employee.selectedIndex];
    employeeName.value = selectedOption.dataset.name;
});

// Show the first employee's name when the page loads
window.onload = function () {
    const selectedOption = employee.options[employee.selectedIndex];
    employeeName.value = selectedOption.dataset.name;
};

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        let filter = this.value.toLowerCase();

        let table = document.getElementById("assignmentTable");

        let rows = table.getElementsByTagName("tr");

        for (let i = 1; i < rows.length; i++) {

            let employee = rows[i].cells[0].textContent.toLowerCase();
            let task = rows[i].cells[1].textContent.toLowerCase();

            if (employee.includes(filter) || task.includes(filter)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    });

}

setTimeout(function(){

    const flashes = document.querySelectorAll(".flash");

    flashes.forEach(function(flash){
        flash.style.display = "none";
    });

}, 3000);