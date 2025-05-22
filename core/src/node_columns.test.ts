import { describe, test, expect } from 'vitest';
import { get_node_columns } from './node_columns';
import { ResourceEdge } from "./resource_edge";

describe("get_node_columns", ()=>{
    test("group one edge into two columns", ()=>{
        let output = get_node_columns({
            "randomid1": new ResourceEdge("a", "b", 9999),
        });
        expect(output).toStrictEqual({
            "a": 0,
            "b": 1,
        });
    });
    test("group two edges into three columns", ()=>{
        let output = get_node_columns({
            "randomid1": new ResourceEdge("a", "b", 9999),
            "randomid2": new ResourceEdge("b", "c", 9999),
        });
        expect(output).toStrictEqual({
            "a": 0,
            "b": 1,
            "c": 2,
        });
    });
    test("group two edges into two columns", ()=> {
        let output = get_node_columns({
            "randomid1": new ResourceEdge("a", "b", 9999),
            "randomid2": new ResourceEdge("a", "c", 9999),
        });
        expect(output).toStrictEqual({
            "a": 0,
            "b": 1,
            "c": 1,
        });
    });
    test("put the last node of an edge chain in the last column", ()=> {
        let output = get_node_columns({
            "randomid1": new ResourceEdge("a", "b", 9999),
            "randomid2": new ResourceEdge("b", "c", 9999),
            "randomid3": new ResourceEdge("d", "e", 9999),
        });
        expect(output).toStrictEqual({
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 0,
            "e": 2
        });
    });
    test("fills in columns from the left when possible", ()=> {
        let output = get_node_columns({
            "randomid1": new ResourceEdge("a", "b", 9999),
            "randomid2": new ResourceEdge("b", "c", 9999),
            "randomid3": new ResourceEdge("c", "d", 9999),
            "randomid4": new ResourceEdge("e", "f", 9999),
            "randomid5": new ResourceEdge("f", "g", 9999),
        });
        expect(output).toStrictEqual({
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,

            "e": 0,
            "f": 1,
            "g": 3,
        });
    });
});
