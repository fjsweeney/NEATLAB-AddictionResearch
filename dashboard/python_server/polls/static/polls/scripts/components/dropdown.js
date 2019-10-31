/*

    'options' is an object in the form of:
    {
        name: string
        menuItems: [] of strings
    }

*/

export default function dropdown(options)
{

    function behavior()
    {
        // alert("hello")
    }

    return({
        template: `<select ${options.name ? `name=${options.name}`: ``}>
                ${options.menuItems.map(item => `<option value=${item}>${item}</option>`).join('')}
            </select>`,
        behavior
    });
}
