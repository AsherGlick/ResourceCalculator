import { describe, test, expect } from 'vitest';
import { __internal__ } from './recipe_info';
const depth_first_search = __internal__.depth_first_search;


describe("depth_first_search", ()=>{
    test("can find a node", ()=>{
        let result = depth_first_search(
            {
                'a': ['b'],
                'b': ['c'],
                'c': ['d'],
                'd': ['e'],
                'e': ['f'],
                'f': ['g'],
                'g': [],
            },
            'a',
            'g'
        );
        expect(result).toStrictEqual(['f']);
    });
    test("short loop", ()=>{
        let result = depth_first_search(
            {
                'a': ['b'],
                'b': ['a'],
            },
            'a',
            'a'
        );
        expect(result).toStrictEqual(['b']);
    });
    test("self loop", ()=>{
        let result = depth_first_search(
            {
                'a': ['a'],
            },
            'a',
            'a'
        );
        expect(result).toStrictEqual(['a']);
    });
});
