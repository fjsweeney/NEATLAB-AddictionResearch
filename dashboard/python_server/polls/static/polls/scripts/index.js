import dropdown from './components/dropdown.js';

if(document.getElementById('loggedInHeaderDropdown'))
{
    patchScript.registerContainers('loggedInHeaderDropdown');

    patchScript.createComponent(dropdown({
        name: "loggedInHeaderDropdown",
        menuItems: ['Public Data', 'Account Settings']
    }), 'loggedInHeaderDropdown');
}
