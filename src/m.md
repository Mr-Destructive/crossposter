---
title: "Configure Neovim in Lua"
description: "something"
canonical_url: "https://www.meetgor.com/neovim-config-lua"
cover_image: "https://res.cloudinary.com/techstructive-blog/image/upload/v1656522785/blog-media/defer-golang-16.png"
published: false
---

## Introduction

It has been a while since I have written a Vim article. Finally, I got some ideas after configuring my Neovim setup for Lua. I recently migrated to Ubuntu a couple of months back and it has been a cool change from Windows 7! 

In this article, we'll see how you can set up neovim for Lua. Since Neovim 0.5, it supports lua out of the box, so in the recent release 0.7, it added more native support to lua making it a lot easier to configure and play with neovim. So, we will see how we can use lua to convert all the 200 liner vimscript into lua (We can even have packages and modules:) We will cover how to configure your keymaps, pull up all the plugins, vim options, and other customizations.

## Why move to Lua?

I have used Vimscript for quite a while now, configured it as per my needs, and also made a few plugins like [frontmatter](https://github.com/Mr-Destructive/frontmatter.vim), [dj.vim](https://github.com/Mr-Destructive/dj.vim), and [commenter](https://github.com/Mr-Destructive/commenter.vim) which are quite clunky and not robust in terms of usage and customizability. Vimscript is good but it's a bit messy when you want extreme customization. 

I recently wanted to go full Neovim, I was kind of stuck in Vimscript and some of my plugins work for me but it might not work for others, it might be a piece of gibberish vimscript dumped. So, Why not have full native experience in Neovim if you can. It has now baked-in support for LSP, Debugging, Autocommands, and so much more. If you have Neovim 0.5+ you should be good to go full lua.

## Backup Neovim Config

Firstly, keep your original neovim/vim init files safe, back them up, make a copy and save it with a different name like `nvim_config.vim`. If you already have all your config files backed up as an ansible script or dotfiles GitHub repository, you can proceed ahead. 

But don't keep the `init.vim` file as it is in the `~/.config/nvim` folder, it might override after we configure the lua scripts.

## Basic Configuration

So, I assume you have set up Neovim, If not you need to follow some simple steps like downloading the package and making sure your neovim environment is working with vimscript first. The [Neovim Wiki](https://github.com/neovim/neovim/wiki/Installing-Neovim) provides great documentation on how to install neovim on various platforms using different methods.

After your neovim is set up and you have a basic configuration, you can now start to migrate into lua.
Create a `init.lua` file in the same path as your `init.lua` file is i.e. at `~/.config/nvim` or `~/AppData/Local/nvim/` for Windows. That's why it is recommended to keep the initial configuration vimscript file in a safe place. While migrating from vimscript to lua, once the lua file is created and the next time you restart neovim, the default settings will be from `init.lua` and not `init.vim`, so be prepared.

Firstly, you need to configure some options like `number`, `syntax highlighting`, `tabs`, and some `keymaps` of course. We can use the `vim.opt` method to set options in vim using lua syntax. So, certain corresponding vim options would be converted as follows:

If you have the following kind of settings in your vimrc or init.vim:

```vimscript
-- vimscript
set number
set tabstop=4 
set shiftwidth=4 
set softtabstop=0 
set expandtab 
set noswapfile
```
The above settings are migrated into lua syntax as follows:

```lua
--lua
vim.opt.number = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.softtabstop = 0
vim.opt.expandtab = true
vim.opt.swapfile = false
```

You can set other options in your config file accordingly. If you get sick of writing `vim.opt.` again and again, you can use a variable set to `vim.opt` and then access that variable to set the options. Something of the lines as below:

```lua
local set = vim.opt

set.number = true
set.tabstop = 4
set.shiftwidth = 4
set.softtabstop = 0
set.expandtab = true
set.swapfile = false
```

We can create a variable in lua like `local variable_name = something` so, we have created a variable `set` which is assigned to the value of `vim.opt` which is a method(function) in lua to set the options from the vimscript environment. Finally, access the `set` keyword to set the options. Using the `set` word is not necessary, you can use whatever you want. 

After setting up the basic options, you can source the file with `:so %` from the command mode. Just normally as you source the config files.

### Using Lua in Command Mode

We can use the lua functions or any other commands from the command mode in neovim using the lua command. Just prefix the command with `:lua` and after that, you can use lua syntax like function calling or setting variables, logging things, etc.

![Lua in Command Mode](https://res.cloudinary.com/techstructive-blog/image/upload/v1657380885/blog-media/lua_in_command_mode.gif)

## Adding Keymaps

Now, that we have some basic config setup, we can quickly get the keymaps. It's not that hard to make keymaps to set up in lua. To create keymaps, we have two options. One is compatible with Neovim and the other is compatible with Vim as well.

1. vim.keymap.set OR 
2. vim.api.nvim_set_keymap

Personally, I don't see a difference in terms of usage but [vim.keymap.set](https://github.com/neovim/neovim/blob/master/runtime/lua/vim/keymap.lua#L51) is a wrapper around [nvim_set_keymap](https://github.com/neovim/neovim/blob/master/src/nvim/api/vim.c#L1451). So, it is really a matter of personal preference which you want to use. 

So, both the functions have quite similar parameters:

```lua
vim.keymap.set({mode}, {lhs}, {rhs}, {options})

vim.api.nvim_set_keymap({mode}, {lhs}, {rhs}, {options})
```

The advantage of `vim.keymap.set` over `vim.api.nvim_set_keymap` is that it allows directly calling lua functions rather than calling vimscripty way like `:lua function()`, so we directly can use lua code in the RHS part of the function parameter.

Let's take a basic example mapping:

```
vim.keymap.set('n', 'Y', 'yy', {noremap = false})
```

Here, we have mapped `Shift+y` with the keys `yy` in `n`ormal mode. The first argument is the mode, it can be a single-mode like `'n'`, `'v'`, `'i'`, etc., or a multi-mode table like `{'n', 'v'}`, `{'v', 'i'}`, etc. 

The next parameter is also a string but it should be the key for triggering the mapping. In this case, we have used `Y` which is `Shift + y`, it can be any key shortcut you want to map.

The third parameter is the string which will be the command to be executed after the key has been used. Here we have used the keys `yy`, if the map is from a command mode, you will be using something like `':commands_to_be executed'` as the third parameter.

The fourth parameter which is optional can contain [special arguments](https://neovim.io/doc/user/api.html#:~:text=nvim_set_keymap(%7Bmode%7D%2C%20%7Blhs%7D%2C%20%7Brhs%7D%2C%20%7B*opts%7D)%20%20%20%20%20%20%20%20%20%20%20%20%20*nvim_set_keymap()*). We have set a default option which is `noremap` as true, the options are not string but lua tables instead, so it can be similar to python dictionary or a map kind of a structure with a key value pair.


One more important aspect in keymapping might about the leader key, you can set your leader key by using the global vim options with `vim.g` and access `mapleader` to set it to the key you wish. This will make the `leader` key available to us and thereafter we can map the leader key in custom mappings.

```
vim.g.mapleader = " "
```

Here, I have set my leader key to the `<Space>` key. Now, we can map keys to the existing keymaps in the vimscript. Let's map some basic keymaps first and then after setting up the plugins,we can move into plugin-specific mappings.

You can also use `vim.api.nvim_set_keymap` function with the same parameters as well. 

```lua
vim.keymap.set('n', '<leader>w', ':w<CR>',{noremap = true})
vim.keymap.set('n', '<leader>q', ':q!<CR>',{noremap = true})
vim.keymap.set('n', '<leader>s', ':so %<CR>',{noremap = true})
vim.keymap.set('n', '<leader>ev', ':vsplit $MYVIMRC<CR>',{noremap = true})
vim.keymap.set('n', '<leader>sv', ':w<CR>:so %<CR>:q<CR>',{noremap = true})

OR

vim.api.nvim_set_keymap('n', '<leader>w', ':w<CR>',{noremap = true})
vim.api.nvim_set_keymap('n', '<leader>q', ':q!<CR>',{noremap = true})
vim.api.nvim_set_keymap('n', '<leader>s', ':so %<CR>',{noremap = true})
vim.api.nvim_set_keymap('n', '<leader>ev', ':vsplit $MYVIMRC<CR>',{noremap = true})
vim.api.nvim_set_keymap('n', '<leader>sv', ':w<CR>:so %<CR>:q<CR>',{noremap = true})
```

If, you don't like writing `vim.keymap.set` or `vim.api.nvim_set_keymap` again and again, you can create a simpler function for it. In lua a function is created just like a variable by specifying the scope of the function i.e. local followed by the `function` keyword and finally the name of the function and parenthesis. The function body is terminated by the `end` keyword.

```lua
function map(mode, lhs, rhs, opts)
    local options = { noremap = true }
    if opts then
        options = vim.tbl_extend("force", options, opts)
    end
    vim.api.nvim_set_keymap(mode, lhs, rhs, options)
end
```
Now, in this function `map`, we have passed in the same parameters like the `vim.keymap.set` function takes but we have just parsed the function in a shorter and safer way by adding `noremap = true` by default. So this is just a helper function or a verbose function for calling the vim.keymap.set function.

To use this function, we can simply call `map` with the same arguments as given to the prior functions.

```lua
map('n', '<leader>w', ':w<CR>')
map('n', '<leader>q', ':q!<CR>')
map('n', '<leader>s', ':so %<CR>')
```

Notice here, though, we have not passed the `{noremap = true}` as it will be passed by default to the `vim.api.nvim_set_keymap` or `vim.keymap.set` function via the custom map function.

If you want some more examples, here are some additional mapping specific to languages, meant for compiling or running scripts with neovim instance. 

```lua
-- vimscript

nnoremap cpp :!c++ % -o %:r && %:r<CR>
nnoremap c, :!gcc % -o %:r && %:r<CR>
nnoremap py :!python %<cr>
nnoremap go :!go run %<cr>
nnoremap sh :!bash %<CR>


-- lua

map('n', 'cpp' ':!c++ % -o %:r && %:r<CR>')
map('n', 'c,' ':!gcc % -o %:r && %:r<CR>')
map('n', 'py' ':!python %<cr>')
map('n', 'go' ':!go run %<cr>')
map('n', 'sh' ':!bash %<cr>')

```

So, this is how we can set up our keymaps in lua. You can customize this function as per your needs. These are just made for the understanding purpose of how to reduce the repetitive stuff in the setup.

**If you are really stuck up and not feeling to convert those mappings into lua then I have a function that can do it for you, check out my dotfile repo -> [keymapper](https://github.com/Mr-Destructive/dotfiles/blob/master/nvim/lua/destructive/options.lua#L9)**

## Adding Plugin Manager

Now, we really missing some plugins, aren't we? So, the neovim community has some good choices for using a new plugin manager written in core lua. It is usually a good idea to move into lua completely rather than switching to and fro between vimscript and lua.

So, [Packer](https://github.com/wbthomason/packer.nvim) is the new plugin manager for Neovim in Lua, there is other plugin managers out there as well like [paq](https://github.com/savq/paq-nvim). If you don't want to switch with the plugin manager, you can still use vim-based plugin managers like [Vim-Plug](https://dev.to/vonheikemen/neovim-using-vim-plug-in-lua-3oom).

So, let's install the Packer plugin manager into Neovim. We simply have to run the following command in the console and make sure the plugin manager is configured correctly.

```
# Linux

git clone --depth 1 https://github.com/wbthomason/packer.nvim\
~/.local/share/nvim/site/pack/packer/start/packer.nvim


# Windows

git clone https://github.com/wbthomason/packer.nvim "$env:LOCALAPPDATA\nvim-data\site\pack\packer\start\packer.nvim"
```

Now, if you open a new neovim instance and try to run the command `:PackerClean`, and no error pops out that means you have configured it correctly. You can move ahead to installing plugins now. Yeah! PLUG-IN time! 

```lua
return require('packer').startup(function()
end)
```

First try to source the file, if it throws out errors it shouldn't try to fix the installation path of Packer. If the command succeded we can finally pull up some plugins.

Below are some of the plugins that you can use irrespective of what language preferences you would have. This includes basic dev-icons for the status line as well as the explorer window file icons. As usual, add your plugins and make them yours.

```lua

return require('packer').startup(function()
  use 'wbthomason/packer.nvim'
  use 'tpope/vim-fugitive'
  use {
    'nvim-lualine/lualine.nvim',
    requires = { 'kyazdani42/nvim-web-devicons', opt = true }
  }
  use 'tiagofumo/vim-nerdtree-syntax-highlight'
  use 'kyazdani42/nvim-web-devicons'
  use 'vim-airline/vim-airline'
  use 'vim-airline/vim-airline-themes'
end)
```

After adding the list of your plugins, you need to source the file and then install the plugins with the command `:PackerInstall`. This function will install all the plugins after the file has been sourced so make sure you don't forget it.

## Colors and Color Themes

You might fancy some good-looking and aesthetic setup for neovim of course! In Neovim, we already have a wide variety of configurations to set up like color schemes, GUI colors, terminal colors, etc. You can pick up a color scheme from a large list of awesome color schemes from [GitHub](https://github.com/topics/neovim-colorscheme). 

After choosing the theme, plug it in the packer plugin list which we just created and source the file and finally run `:PackerInstall`. This should install the plugin. You can then set the colorscheme as per your preference, first view the color scheme temporarily on the current instance with the command `:colorscheme colorscheme_name`. 

```lua
return require('packer').startup(function()
  use 'wbthomason/packer.nvim'
  -- 
  use 'Mofiqul/dracula.nvim'
  --
end)
```

You can then add the command to set it as the default color scheme for Neovim.

```lua
vim.cmd [[silent! colorscheme dracula]]
```

You can change the background color, text color, icons style and terminal and gui style separately with the augroup and setting the colorscheme commands.

```lua
vim.api.nvim_command([[
    augroup ChangeBackgroudColour
        autocmd colorscheme * :hi normal termbg=#000030 termfg=#ffffff
        autocmd colorscheme * :hi Directory ctermfg=#ffffff
    augroup END
]])
vim.o.termguicolors = true
```

Here, I have used the background and foreground colors of the terminal variant of Neovim. Also for the Directory Explorer i.e. netrw, I have changed the terminal foreground. This you can configure as per your needs, Though this is still vimscripty, there are Autocommands and autogroups available sooner in Neovim.

## Separating Configurations

If you wish to keep all your config in one file i.e. `init.lua` file, you can, though you can separate out things like `keymaps`, `plugins`, `custom_options` or if you have `lsp` configurations into separate lua packages or creating a separate module. This helps in loading up things as per requirement and also looks readable, making it a lot easier to test out things without breaking the whole config. 

Definitely, there will be personal preferences and pros and cons of both approaches, you can pick up whatever suits your style.

### Creating separate packages 

To create a separate package, we can simply add a file in the same folder as `init.vim` i.e. in the folder `~/.config/nvim` or equivalent for windows. The package name can be any valid filename with the `lua` extension. 

For instance, you can create a package for all your keymaps and load it in the `init.lua` as per the order you want to load them. It can be at the top, or else if you have certain base settings lower in the init file, these might not reflect or load up in the keymap package so better to load them after some of the core settings have been set.

Let's create the package and dump all our maps into the keymap file package.

```lua
-- ~/.config/nvim/keymap.lua

function map(mode, lhs, rhs, opts)
    local options = { noremap = true }
    if opts then
        options = vim.tbl_extend("force", options, opts)
    end
    vim.api.nvim_set_keymap(mode, lhs, rhs, options)
end

map('n', '<leader>w', ':w<CR>')
map('n', '<leader>q', ':q!<CR>')
map('n', '<leader>s', ':so %<CR>')
map('n', 'cpp' ':!c++ % -o %:r && %:r<CR>')
map('n', 'c,' ':!gcc % -o %:r && %:r<CR>')
map('n', 'py' ':!python %<cr>')
map('n', 'go' ':!go run %<cr>')
map('n', 'sh' ':!bash %<cr>')

-- more keymaps

```

So, this might work if you don't have any plugin-related keymaps as it would require those functions or objects available to execute. So, we might also want to separate plugins and load them first in our keymaps or in the init file.

Now, there needs to be a way for grabbing a package. Yes, there is basically like import in python or any other programming language, lua has `require` keyword for importing packages. Since the `init` file and the `keymaps` are in the same folder path, we can simply say, `require("keymap")` in our `init.lua` file. Now, it depends on your config where you want to load this package. At the top i.e. at the beginning of neovim instance or after loading the plugins down.

```lua
-- init.lua

require("keymaps")

-- At the top
-- OR
-- After loading Packer plugins
```

So, now you can separate all your configs as per your requirement. It is like splitting up a puzzle and again combining them. Similar package can be created for `plugins`, `options` or `lsp` configurations.

### Creating a separate module

Now, we have seen how to create a lua package and loading in neovim. We also can create modules in neovim configuration. For instance, first, the init file is loaded, Other files might not be required hence it is not loaded by default, it is only loaded when `require`ed. So, we can create a module in lua with a folder, and inside of it, we can have packages as we had in the previous method. Also, every module can have a init file loaded first when we require that module. The rest of the packages in the module are thus made available thereafter.

- Module is a component not loaded by default
- Only loaded when required (literally require)
- Every module can have a `init.lua` file loaded first when required.
- Require a package in module from outside -> `require('module_name.package_name')`

So, in neovim, we need to create a `lua` folder for placing all our modules so that the lua runtime is picked up correctly. Inside this lua folder, we can create a module basically a folder. This folder name can be anything you like, I like to keep it my nickname, you can use whatever you prefer. 

```
# ~/.config/nvim

-- init.lua
-- lua/
    -- module_name/
        -- init.lua
        -- package_name.lua
        -- keymaps.lua
```

Now, we can create packages in this module. You can move your keymaps package inside this folder. The keymaps package is nothing here but an example provided in the previous section for creating a package. You can basically dump all your keymaps in a single lua file and then import it from the init file. Similarly you can create a package inside a module and import it from the init file of the module(local init file `~/.config/nvim/lua/module_name/init.lua`) or the global init file(`~/.config/nvim/init.lua`). 

To load the packages, you have to use the same require statement irrespective of where you are importing from i.e. either from the module or from the global init file. The require statement would look like the following `require("module_name/package_name")`. Now, we can use the keymaps package to import from the module init file and then import the module from the global init file. To import a module, we can simply use the module name in the require string as `require("module_name")`.

```lua
-- ~/.config/nvim

-- lua/module_name/options.lua

vim.opt.number = true
vim.opt.tabstop = 4
vim.opt.swapfile = false


-- lua/module_name/plugins.lua

require("module_name.options")
return require('packer').startup(function()
  use 'wbthomason/packer.nvim'
  --plugins
end)

-- lua/module_name/keymap.lua

require("module_name.plugins")
-- maps()


-- lua/module_name/init.lua

require("module_name.keymaps)


-- init.lua

require("module_name")

```

So, this is how we can create modules and packages for configurations in neovim using lua. This is also a kind of a structure for creating your own neovim plugin with lua!

For further references, you can check out my [dotfiles](https://github.com/Mr-Destructive/dotfiles). 
### References

- [Configure Neovim for Lua](https://vonheikemen.github.io/devlog/tools/configuring-neovim-using-lua/)
- [Neovim with Lua for beginners](https://alpha2phi.medium.com/neovim-for-beginners-init-lua-45ff91f741cb)
- [TJ Devries Youtube](https://www.youtube.com/c/TJDeVries/videos)

## Conclusion

So, that is just a basic overview of how you can get your neovim configured for lua. It is a great experience to just create such a personalized environment and play with it and have fun. You might have hopefully configured Neovim for Lua from this little guide. Maybe in the next article, I'll set up LSP in Neovim. If you have any queries or feedback, please let me know. Thank you for reading.

Happy Viming :)