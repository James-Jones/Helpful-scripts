from pyassimp import pyassimp
import argparse
import os
import types
import array
import json

# Define the command line arguments
parser = argparse.ArgumentParser(description='Convert assimp meshes.')
parser.add_argument("-f", "--file", dest="filename", required=True, help="input file")
parser.add_argument("-j", "--json", dest="bJSON", action='store_true', help="output in JSON")

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

def writeMeshJSON(mesh, material, transform):
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

    # Texcoords
    
    texcarray = array.array('f')
    
    for texc in enumerate(mesh.texcoords[0]):
        texcarray.extend(texc[1])

    # Normals
    
    nrmarray = array.array('f')
    
    for nrm in enumerate(mesh.normals):
        nrmarray.extend(nrm[1])
        
    # Indices
    idxarray = array.array('H')

    for face in enumerate(mesh.faces):
        idxarray.extend(face[1].indices)

    matrix = [transform.a1,
    transform.a2,
    transform.a3,
    transform.a4,
    transform.b1,
    transform.b2,
    transform.b3,
    transform.b4,
    transform.c1,
    transform.c2,
    transform.c3,
    transform.c4,
    transform.d1,
    transform.d2,
    transform.d3,
    transform.d4]

    bbox = getBoundingBox(mesh)
    
    materialName = pyassimp.aiGetMaterialString(material, ["?mat.name",0,0])
    diffuseTexName = pyassimp.aiGetMaterialString(material, ["$tex.file",1,0])
    try:
        diffuseColour = pyassimp.aiGetMaterialFloatArray(material, ["$clr.diffuse",0,0])
    except:
        print "No diffuse colour"
    ambientColour = pyassimp.aiGetMaterialFloatArray(material, ["$clr.ambient",0,0])
    specularColour = pyassimp.aiGetMaterialFloatArray(material, ["$clr.specular",0,0])
    try:
        emissiveColour = pyassimp.aiGetMaterialFloatArray(material, ["$clr.emissive",0,0])
    except:
        print "No emissive colour"
    shininess = pyassimp.aiGetMaterialFloatArray(material, ["$mat.shininess",0,0])
    try:
        reflectivity = pyassimp.aiGetMaterialFloatArray(material, ["$mat.reflectivity",0,0])
    except:
        print "No reflectivity"
    try:
        shininessStength = pyassimp.aiGetMaterialFloatArray(material, ["$mat.shinpercent",0,0])
    except:
        print "No shininess strength"

    # Format as a list
    mylist = {  "bndbox": bbox,
                "vtxpos": list(vtxarray),
                "texcoord": list(texcarray),
                "normal": list(nrmarray),
                "idx": list(idxarray),
                "transform": matrix,
                "ambient": ambientColour,
                "diffise": diffuseColour,
                "diffuseTex": diffuseTexName}
    
    # dummylist = {"vtxpos" : [0.0, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0], "idx" : [0, 1, 2] }

    # Convert python list to JSON and write to file
    json.dump(mylist, outputfile, indent=4)

    outputfile.write("\n");

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
            writeMeshJSON(mesh, scene.materials[mesh.mMaterialIndex], scene.mRootNode[0].mTransformation)
        else:
            writeMesh(mesh)
    
    # Finally release the model
    pyassimp.release(scene)

if __name__ == "__main__":
    main()