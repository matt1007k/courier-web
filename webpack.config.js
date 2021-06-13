module.exports = {
	resolve: {
        extensions: [".tsx", ".ts", ".js"],
    },
	watch: true,
	module: {
	  rules: [
		{
		  test: /\.(js|jsx)$/,
		  exclude: /node_modules/,
		  use: {
			loader: "babel-loader"
		  }
		},
		{
			test: /\.(ts|tsx)$/,
			exclude: /node_modules/,
			use: ["ts-loader"],
		},
	  ]
	}
};