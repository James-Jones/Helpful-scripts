from pyassimp import pyassimp
import argparse
import os
import types
import array
import json

# Define the command line arguments
parser = argparse.ArgumentParser(description='Convert assimp meshes.')
parser.add_argument("-f", "--file", dest="filename", required=True, help="input file")
parser.add_argument("-j", "--json", dest="bJSON", help="output in JSON")

# Parse the arguments
options = parser.parse_args()

# From include/aiPostProcess.h
aiProcess_CalcTangentSpace = 0x1
aiProcess_JoinIdenticalVertices = 0x2
aiProcess_Triangulate = 0x8
aiProcess_GenSmoothNormals = 0x40
aiProcess_ImproveCacheLocality = 0x800
aiProcess_OptimizeMeshes = 0x200000

aiProcessFlags = aiProcess_CalcTangentSpace | aiProcess_JoinIdenticalVertices | aiProcess_Triangulate | aiProcess_GenSmoothNormals | aiProcess_ImproveCacheLocality | aiProcess_OptimizeMeshes

def getBoundingBox(mesh):
    boxmin = [1e10, 1e10, 1e10]
    boxmax = [-1e10, -1e10, -1e10]
    
    for vtx in enumerate(mesh.vertices):
        boxmin[0] = min(boxmin[0], vtx[1].x)
        boxmin[1] = min(boxmin[1], vtx[1].y)
        boxmin[2] = min(boxmin[2], vtx[1].z)
        
        boxmax[0] = max(boxmax[0], vtx[1].x)
        boxmax[1] = max(boxmax[1], vtx[1].y)
        boxmax[2] = max(boxmax[2], vtx[1].z)
    
    result = boxmin
    result.extend(boxmax)
    return result

def writeMeshJSON(mesh):
    # The output filename is the input filename with a .bin extension
    basename, extension = os.path.splitext(options.filename)
    (head, tail) = os.path.split(options.filename);
    basetail = os.path.splitext(tail)[0]
    outputfilename = basename + ".json"
    
    # Create the output file. Write-only
    
    outputfile = open(outputfilename, "wb")
    f32val = 1.0
    s = str(f32val)

    # Header
    
    header = array.array('H', [len(mesh.vertices), len(mesh.faces)])
    # header.tofile(outputfile);
    
    # Vertices
    
    vtxarray = array.array('f')
    
    for vtx in enumerate(mesh.vertices):
        vtxarray.extend(vtx[1])

    # Indices
    idxarray = array.array('H')

    for face in enumerate(mesh.faces):
        idxarray.extend(face[1].indices)

    bbox = getBoundingBox(mesh)

    # Format as a list
    mylist = {"bndbox": bbox, "vtxpos": list(vtxarray), "idx": list(idxarray)}
    
    # dummylist = {"vtxpos" : [0.0, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0], "idx" : [0, 1, 2] }

    # Convert python list to JSON and write to file
    json.dump(mylist, outputfile, indent=4)

    # Closing brace
    #outputfile.write("\n}\n");

    # Cleanup
    outputfile.close()

def writeMesh(mesh):
    # The output filename is the input filename with a .bin extension
    basename, extension = os.path.splitext(options.filename)
    (head, tail) = os.path.split(options.filename);
    basetail = os.path.splitext(tail)[0]
    outputfilename = basename + ".bin"
    
    # Create the output file. Write-only
    
    outputfile = open(outputfilename, "wb")
    f32val = 1.0
    s = str(f32val)
    
    # Header
    
    header = array.array('H', [len(mesh.vertices), len(mesh.faces)])
    header.tofile(outputfile);
    
    # Vertices
    
    vtxarray = array.array('f')
    
    for vtx in enumerate(mesh.vertices):
        vtxarray.extend(vtx[1])
        
    vtxarray.tofile(outputfile)
    
    # Indices
    idxarray = array.array('H')
    
    for face in enumerate(mesh.faces):
        idxarray.extend(face[1].indices)

    idxarray.tofile(outputfile)

    # Cleanup
    outputfile.close();

def main():
    scene = pyassimp.load(options.filename, aiProcessFlags)
    
    for index, mesh in enumerate(scene.meshes):
        if(options.bJSON):
            writeMeshJSON(mesh)
        else:
            writeMesh(mesh)
    
    # Finally release the model
    pyassimp.release(scene)

if __name__ == "__main__":
    main()