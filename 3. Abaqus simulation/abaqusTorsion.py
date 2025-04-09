# -*- coding: mbcs -*-
# Do not delete the following import lines
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
        p = mdb.models['Model-1'].parts['Beam1']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        region = p.Set(cells=cells, name='Set-1')
        p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
        
        # Create assembly and instance
        a = mdb.models['Model-1'].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models['Model-1'].parts['Beam1']
        a.Instance(name='Beam1-1', part=p, dependent=ON)
        
        # Create step
        mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
        
        # Apply BCs
        a = mdb.models['Model-1'].rootAssembly
        f1 = a.instances['Beam1-1'].faces
        
        # Bottom face BC (Fully or partially fixed)
        faces1 = f1.findAt(((point[0], point[1], 0),))
        region = a.Set(faces=faces1, name='Set-1')
        # Keep the bottom face constraints as before
        mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1', 
            region=region, u1=0.0, u2=0.0, u3=UNSET, ur1=UNSET, ur2=0.0, ur3=0.0, 
            amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
            localCsys=None)
        
        # Top face: Instead of a simple displacement BC, we apply a rotation
        faces_top = f1.findAt(((point[0], point[1], 1000.0),))
        top_face_region = a.Set(faces=faces_top, name='Set-2')

        # Create a reference point and couple it to the top face
        rp = a.ReferencePoint(point=(point[0], point[1], 1000.0))
        rpRegion = a.Set(referencePoints=(a.referencePoints[rp.id],), name='RP')

        # Coupling: Kinematic coupling between RP and top face
        mdb.models['Model-1'].Coupling(name='Couple-RP-TopFace', 
            controlPoint=rpRegion, surface=top_face_region, influenceRadius=WHOLE_SURFACE, 
            couplingType=KINEMATIC, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

        # Apply a rotational displacement at the reference point
        # For example, rotate about the 3rd axis (ur3) by 0.2 radians
        mdb.models['Model-1'].DisplacementBC(name='BC-Rotation', createStepName='Step-1', 
            region=rpRegion, u1=UNSET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=0.2)
        
        # Generate mesh
        p = mdb.models['Model-1'].parts['Beam1']
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
        session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
            engineeringFeatures=OFF, mesh=ON)
        session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
            meshTechnique=ON)
        p = mdb.models['Model-1'].parts['Beam1']
        p.seedPart(size=50.0, deviationFactor=0.1, minSizeFactor=0.01)
        p = mdb.models['Model-1'].parts['Beam1']
        p.seedPart(size=50.0, deviationFactor=0.1, minSizeFactor=0.001)
        p = mdb.models['Model-1'].parts['Beam1']
        p.seedPart(size=10.0, deviationFactor=0.1, minSizeFactor=0.001)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=1846.38, 
            farPlane=2579.49, width=299.684, height=134.185, viewOffsetX=-272.012, 
            viewOffsetY=-129.67)
        p = mdb.models['Model-1'].parts['Beam1']
        p.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.001)
        session.viewports['Viewport: 1'].view.setValues(nearPlane=1750.29, 
            farPlane=2675.59, width=1534.94, height=687.279, viewOffsetX=-20.3906, 
            viewOffsetY=-54.5182)
        p = mdb.models['Model-1'].parts['Beam1']
        p.generateMesh()
        session.viewports['Viewport: 1'].view.setValues(nearPlane=1798, 
            farPlane=2627.88, width=903.485, height=404.541, viewOffsetX=-128.406, 
            viewOffsetY=-86.2053)
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
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
            CONTOURS_ON_DEF, ))
        
        # Customize display settings
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
            visibleEdges=FEATURE)
        session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
            triad=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
        session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
            variableLabel='S', outputPosition=INTEGRATION_POINT, 
            refinement=(INVARIANT, 'Mises'), )
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
            deformationScaling=UNIFORM, uniformScaleFactor=1)
        
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxAutoCompute=OFF, minAutoCompute=OFF)
    
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(maxValue=1e3, minValue=0)
    

        # Ensure the contour plot uses the defined spectrum range
        #session.spectrum('Blue to Red').setValues(maxValue=5e11, minValue=1e8)

        # Save the viewport image
        image_filename = '/{}.png'.format(filename)
        session.printToFile(fileName=image_filename, format=PNG, canvasObjects=(session.viewports['Viewport: 1'],))


        # Open the .odb file
        odb = openOdb(path='C:/temp/Job-1.odb')

        # Access the last frame of the last step
        lastFrame = odb.steps['Step-1'].frames[-1]

        # Access the stress field output
        stressField = lastFrame.fieldOutputs['S']

        # Initialize lists to store the von Mises, tensile, and compressive stresses
        vonMisesList = []
        tensileList = []
        compressiveList = []

        # Loop through each value in the stress field output
        for stressValue in stressField.values:
            # Update von Mises stress list
            vonMisesList.append(stressValue.mises)
            
            # Get the components of the stress tensor
            tensor = stressValue.data

            # Calculate principal stresses
            stressTensor = np.array([[tensor[0], tensor[3], tensor[5]], [tensor[3], tensor[1], tensor[4]], [tensor[5], tensor[4], tensor[2]]])

            principalStresses = np.linalg.eigvalsh(stressTensor)
            
            # Update tensile and compressive stress lists
            tensileList.append(principalStresses.max())
            compressiveList.append(principalStresses.min())

        # Sort the stress lists
        vonMisesList.sort(reverse=True)
        tensileList.sort(reverse=True)
        compressiveList.sort()

        # Compute the average of the top 10 highest values, ignoring the top no. 1 highest value
        averageVonMises = np.mean(vonMisesList[1:11])
        averageTensile = np.mean(tensileList[1:11])
        averageCompressive = np.mean(compressiveList[1:11])

        # Append the results to the beam_results.txt file
        results_file_path = 'torsionResults.txt'
        with open(results_file_path, 'a') as f:
            f.write("{}, VM = {}, Tensile = {}, Compressive = {}\n".format(filename, averageVonMises, averageTensile, averageCompressive))

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
results_file_path = 'torsionResults.txt'
if not os.path.exists(results_file_path):
    with open(results_file_path, 'w') as f:
        f.write("")

# Iterate through each text file and run the Beam function
for txt_file in txt_files:
    txt_file_path = os.path.join(instructions_path, txt_file.strip())
    Beam(txt_file_path)

