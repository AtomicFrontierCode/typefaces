# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
import __main__
from odbAccess import *
import numpy as np
import os

def Beam(fileName):
    try:
        # Read the input file
        with open(fileName, 'r') as file:
            lines = file.readlines()
        
        # Extract parameters from the input file
        params = lines[0].strip().split(', ')
        filename = params[0].split('= ')[1]
        density = float(params[1].split('= ')[1])
        point = float(params[2][9:]), float(params[3][:-1])
        
        # Extract sketch lines
        sketch_lines = lines[1:]
        
        import section
        import regionToolset
        import displayGroupMdbToolset as dgm
        import part
        import material
        import assembly
        import step
        import interaction
        import load
        import mesh
        import optimization
        import job
        import sketch
        import visualization
        import xyPlot
        import displayGroupOdbToolset as dgo
        import connectorBehavior

        s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
            sheetSize=200.0)
        g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
        s.setPrimaryObject(option=STANDALONE)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=155.166, 
            farPlane=221.957, width=497.972, height=228.673, cameraPosition=(
            34.5536, -0.0754834, 188.562), cameraTarget=(34.5536, -0.0754834, 0))
        
        # Add lines to the sketch
        for line in sketch_lines:
            exec(line.strip())
        
        # Make 3D part
        p = mdb.models['Model-1'].Part(name='Beam1', dimensionality=THREE_D, 
            type=DEFORMABLE_BODY)
        p = mdb.models['Model-1'].parts['Beam1']
        p.BaseSolidExtrude(sketch=s, depth=1000.0)
        s.unsetPrimaryObject()
        p = mdb.models['Model-1'].parts['Beam1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        del mdb.models['Model-1'].sketches['__profile__']
        session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
            engineeringFeatures=ON)
        session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
            referenceRepresentation=OFF)
        mdb.models['Model-1'].Material(name='MyMaterial')
        
        # Set material properties
        mdb.models['Model-1'].materials['MyMaterial'].Density(table=((density, ), ))
        mdb.models['Model-1'].materials['MyMaterial'].Elastic(table=((209000.0, 0.3), ))
        
        # Sections
        mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
            material='MyMaterial', thickness=None)
        
        # Assign sections
        session.viewports['Viewport: 1'].view.setValues(nearPlane=1735.75, 
            farPlane=2690.12, width=1941.83, height=867.947, viewOffsetX=-102.925, 
            viewOffsetY=36.8656)
        p = mdb.models['Model-1'].parts['Beam1']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(cells=cells, name='Set-1')
        p = mdb.models['Model-1'].parts['Beam1']
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=1705.52, 
            farPlane=2720.35, width=2132.95, height=953.373, viewOffsetX=-22.1751, 
            viewOffsetY=-26.3117)
        
        # Create assembly and instance
        a = mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        a1 = mdb.models['Model-1'].rootAssembly
        a1.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts['Beam1']
        a1.Instance(name='Beam1-1', part=p, dependent=ON)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(
            adaptiveMeshConstraints=ON)
        
        # Create buckling step with numEigen=2
        mdb.models['Model-1'].BuckleStep(name='Step-1', previous='Initial', numEigen=2, 
                                         vectors=2, maxIterations=200)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
            constraints=ON, connectors=ON, engineeringFeatures=ON, 
            adaptiveMeshConstraints=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
            predefinedFields=ON, interactions=OFF, constraints=OFF, 
            engineeringFeatures=OFF)
        
        # Apply EncastreBC at bottom face (Z=0.0)
        a = mdb.models['Model-1'].rootAssembly
        f1 = a.instances['Beam1-1'].faces
        faces_bottom = f1.getByBoundingBox(zMin=-1e-6, zMax=1e-6)
        region = a.Set(faces=faces_bottom, name='Set-BC')
        mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1', 
            region=region, localCsys=None, buckleCase=PERTURBATION_AND_BUCKLING)
        
        # Apply pressure load on top face (Z=1000.0)
        faces_top = f1.getByBoundingBox(zMin=1000.0 - 1e-6, zMax=1000.0 + 1e-6)
        region = a.Surface(side1Faces=faces_top, name='Surf-Load')
        mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
            region=region, distributionType=TOTAL_FORCE, field='', magnitude=1.0)
        
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
            bcs=OFF, predefinedFields=OFF, connectors=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
            meshTechnique=ON)
        
        # Generate mesh
        p = mdb.models['Model-1'].parts['Beam1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
            engineeringFeatures=OFF, mesh=ON)
        session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
            meshTechnique=ON)
        p = mdb.models['Model-1'].parts['Beam1']
        p.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.001)
        p.generateMesh()
        a1 = mdb.models['Model-1'].rootAssembly
        a1.regenerate()
        a = mdb.models['Model-1'].rootAssembly
        session.viewports['Viewport: 1'].setValues(displayedObject=a)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
            optimizationTasks=ON, geometricRestrictions=ON, stopConditions=ON)
        session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
            meshTechnique=OFF)
        session.viewports['Viewport: 1'].assemblyDisplay.setValues(
            optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
        
        # Create and submit job
        mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
            scratch='', resultsFormat=ODB, numThreadsPerMpiProcess=1, 
            multiprocessingMode=DEFAULT, numCpus=1, numGPUs=1)
        mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
        
        # Wait for the job to complete
        mdb.jobs['Job-1'].waitForCompletion()
        
        # Open the output database and set up the display
        session.mdbData.summary()
        o3 = session.openOdb(name='C:/temp/Job-1.odb')
        session.viewports['Viewport: 1'].setValues(displayedObject=o3)
        session.viewports['Viewport: 1'].makeCurrent()
        
        # Set the frame to the second eigenmode (frame 1)
        session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
        
        # Set deformation scaling
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
            deformationScaling=AUTO)
        
        # Set plot state
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF, ))
        
        # Customize display settings
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
            visibleEdges=FEATURE)
        session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
            triad=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
        
        # Set primary variable with invariant
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='U', outputPosition=NODAL, refinement=(INVARIANT, 'Magnitude'))
        
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, uniformScaleFactor=1e-6)
        
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, minAutoCompute=OFF)
    
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxValue=1, minValue=0)
        
        # Save the viewport image
        image_filename = '/{}.png'.format(filename)
        session.printToFile(fileName=image_filename, format=PNG, canvasObjects=(session.viewports['Viewport: 1'],))
        
        # Open the .odb file
        odb = openOdb(path='C:/temp/Job-1.odb')
        
        # Access the second eigenvalue
        frame = odb.steps['Step-1'].frames[1]  # frame 1 corresponds to Mode 2
        description = frame.description  # 'Mode 2: EigenValue = ...'
        
        # Extract eigenvalue from description
        import re
        match = re.search(r"Eigen[Vv]alue\s*=\s*([-\d\.E+]+)", description)
        if match:
            eigenvalue = float(match.group(1))
        else:
            eigenvalue = None
        
        # Append the results to the beam_results.txt file
        results_file_path = '/bucklingResults.txt'
        with open(results_file_path, 'a') as f:
            f.write("{}, EV = {}\n".format(filename, eigenvalue))
        
        # Close the .odb file
        odb.close()
        
    except Exception as e:
        # Log the error and continue with the next file
        with open('/error_log.txt', 'a') as error_file:
            error_file.write("Error processing file {}: {}\n".format(fileName, str(e)))
        print("Error processing file {}: {}\n".format(fileName, str(e)))

# Read the list of text files
instructions_path = '/'
with open(os.path.join(instructions_path, 'fontsToTest.txt'), 'r') as file_list:
    txt_files = file_list.readlines()

# Ensure the results file exists
results_file_path = 'C/bucklingResults.txt'
if not os.path.exists(results_file_path):
    with open(results_file_path, 'w') as f:
        f.write("")

# Iterate through each text file and run the Beam function
for txt_file in txt_files:
    txt_file_path = os.path.join(instructions_path, txt_file.strip())
    Beam(txt_file_path)

