const path = require('path')
const WebpackBundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')


const plugins = () => {
    const base = [
        new WebpackBundleTracker({
            filename: './webpack-stats.json',
        }),
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: '[name]-[fullhash:16].css'
        }),
    ]
    return base
}


const cssloaders = (extra) => {
    const loaders = [
        {
            loader: MiniCssExtractPlugin.loader,
            options: {
                publicPath: path.resolve(__dirname, 'static/dist')
            },
        },
        'css-loader',
    ]

    if (extra) {
        loaders.push(extra)
    }

    return loaders
}


module.exports = {
    mode: 'development',
    entry: {
        main: './static/ts/main.ts',
    },
    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: '[name]-[fullhash:16].js',
        publicPath: '/static/dist/',
    },
    plugins: plugins(),
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.s[ac]ss$/,
                use: cssloaders('sass-loader')
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js', '.scss', '.css', ],
    }
}
