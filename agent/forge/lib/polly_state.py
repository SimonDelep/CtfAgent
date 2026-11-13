SCHEMA = {
  "name": "polly_state",
  "description": "Calcule state_at(x, seed) pour un seed donné, en utilisant la transformation linéaire du PRNG",
  "parameters": {
    "properties": {
      "seed": {
        "type": "integer"
      },
      "shifts": {
        "items": {
          "type": "integer"
        },
        "type": "array"
      },
      "x": {
        "type": "integer"
      }
    },
    "required": [
      "x",
      "seed",
      "shifts"
    ],
    "type": "object"
  }
}

MASK64 = (1 << 64) - 1

def transform(state, num, shifts):
    if num % 2 == 0:
        state ^= (state << shifts[0]) & MASK64
        state ^= state >> shifts[1]
        state ^= (state << shifts[2]) & MASK64
        state ^= state >> shifts[3]
    else:
        state ^= (state >> shifts[0])
        state ^= (state << shifts[1]) & MASK64
        state ^= (state >> shifts[2])
        state ^= (state << shifts[3]) & MASK64
    return state & MASK64

def transformation(operator, state):
    result = 0
    for bit in range(64):
        if state & (1 << bit):
            result ^= operator[bit]
    return result & MASK64

def square_operator(operator):
    return [transformation(operator, column) for column in operator]

def build_jump_table(shifts, num):
    first_jump = [transform(1 << bit, num, shifts) for bit in range(64)]
    jumps = [first_jump]
    for _ in range(63):
        jumps.append(square_operator(jumps[-1]))
    return jumps

def state_at(x, seed, shifts, num):
    MASK64 = (1 << 64) - 1
    jumps = build_jump_table(shifts, num)
    state = seed & MASK64
    for bit in range(64):
        if x & (1 << bit):
            state = transformation(jumps[bit], state)
    return state & MASK64

def main(args):
    x = args['x']
    seed = args['seed']
    shifts = args['shifts']
    num = args.get('num', 0)
    result = state_at(x, seed, shifts, num)
    print(result)

if __name__ == "__main__":
    import json as _json, sys as _sys
    _args = _json.loads(_sys.argv[1]) if len(_sys.argv) > 1 else {}
    main(_args)
