function Contains(t, elem)
    for _, v in ipairs(t) do
        if v == elem then
            return true
        end
    end
    return false
end

---@param src string
local function make_jl(src)
    local stack = {}
    local jl = {}
    for i = 1, #src do
        local c = src:sub(i, i)
        if c == '[' then
            table.insert(stack, i)
        elseif c == ']' then
            j = table.remove(stack, #stack)

            jl[i] = j
            jl[j] = i
        end
    end
    return jl
end

---@param src string
function Run(src)
    local mem = { 0 }
    local i = 1
    local ptr = 1
    local output = ''
    local jl = make_jl(src)

    while i < #src do
        local c = src:sub(i, i)

        if c == '+' then
            mem[ptr] = mem[ptr] + 1
        elseif c == '-' then
            mem[ptr] = mem[ptr] - 1
        elseif c == '>' then
            ptr = ptr + 1
            if ptr > #mem then
                table.insert(mem, 0)
            end
        elseif c == '<' then
            ptr = ptr - 1
        elseif c == '!' then
            break
        elseif c == '.' then
            output = output .. string.char(mem[ptr])
        elseif c == '[' then
            if mem[ptr] == 0 then
                i = jl[i]
            end
        elseif c == ']' then
            if mem[ptr] ~= 0 then
                i = jl[i]
            end
        end
        i = i + 1
    end

    -- print(output)
    return output
end
