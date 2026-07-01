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