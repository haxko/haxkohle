const webpack = require('webpack');
const path = require('path');


const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  mode: 'production',
  entry: [path.resolve(__dirname, 'main.js')],
  output: { path: __dirname, publicPath: './static/', filename: 'static/bundle.js'},
  module: {
    rules: [{ test: /\.s?css$/, use: ['style-loader',  'css-loader', 'sass-loader']}]
  }
};

