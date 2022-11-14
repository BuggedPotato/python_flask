const getTime  = () => {
    return new Date().toLocaleTimeString( "pl-pl" )
}

const init = () => {
    const el = document.getElementById( "timeNow" );
    setInterval( ()=>{
        el.innerText = getTime();
    }, 333);
}
init();