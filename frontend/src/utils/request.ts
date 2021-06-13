interface OptionsHeaders{
	method: string,
	body?: string;
}

const request = ( url: string, params = {}, method: string = 'GET' ) => {
    const options: OptionsHeaders = {
        method
    };
    if (method === 'GET') {
        url += '?' + ( new URLSearchParams( params ) ).toString();
    } else {
        options.body = JSON.stringify( params );
    }
    
    return fetch( url, options ).then( response => response.json() );
};
export const get = ( url: string, params: object ) => request( url, params, 'GET' );
export const post = ( url: string, params: object ) => request( url, params, 'POST' );
