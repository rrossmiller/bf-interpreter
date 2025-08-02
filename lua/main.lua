require("utils")
print('lua')

local LANG = { "+", "-", "<", ">", "[", "]", ",", ".", "!" }
local src_file = io.open(arg[1])

if src_file == nil then
    os.exit(1)
end

local src = src_file:read("*a")

-- filter the src code
local n = 5000
local start = os.time()
local output
for i = 1, n do
    local ptr = 1
    local src_filtered = ''
    for i = 1, #src do
        local c = src:sub(i, i)
        if Contains(LANG, c) then
            src_filtered = src_filtered .. c
            ptr = ptr + 1
        end
    end

    output = Run(src_filtered)
end

-- time in millis
local e = (os.time() - start) / n * 1000
print(output)
print()
print('elapsed: ' .. e .. ' ms')
