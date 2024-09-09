var project = app.project;

// Function to add a marker at a specific time
function addMarkerToClip(time) {
    project.activeSequence.markers.createMarker(time);
}

// Function to run an external Python script
function runPythonScript(args, projectPath, inPoint, outPoint) {
    // TODO: Change this to *not* be hard-coded
    var argsFile = new File("~/Desktop/PremiereBlippr/args.txt");
    argsFile.open("w");
    argsFile.write('"' + args + '" ');
    // Extract the parent directory of the project path
    projectPath = projectPath.substring(0, projectPath.lastIndexOf("\\"));
    argsFile.write('"' + projectPath + '"');
    argsFile.write(" --in_time " + inPoint.seconds);
    argsFile.write(" --out_time " + outPoint.seconds);
    argsFile.write(" --threshold -50 ");
    argsFile.write(" --chunk_size 1");
    argsFile.write(" --fps 60");
    argsFile.close();
    $.sleep(1000);
    // TODO: Change this to *not* be hard-coded
    var script = new File("~/Desktop/PremiereBlippr/pythonlauncher.bat");
    // Execute and wait for the script to finish
    script.execute();
    // wait until a file called timestamps.json is created
    while (!File("~/Desktop/PremiereBlippr/timestamps.json").exists) {
        $.sleep(1000);
    }
    argsFile.remove();
    // Load the list from timestamps.json
    var timestamps = [];
    var timestampsFile = new File("~/Desktop/PremiereBlippr/timestamps.json");
    timestampsFile.open("r");
    timestamps = timestampsFile.read();
    // convert the JSON string to a JavaScript object list
    timestamps = JSON.parse(timestamps);

    timestampsFile.close();
    timestampsFile.remove();
    return timestamps;
}

// Main Function
function main() {
    var sequence = project.activeSequence;

    if (!sequence) {
        alert("No active sequence found.");
        return;
    }

    // go through all the elements in the sequence and print their names to the console
    for (var i = 0; i < sequence.videoTracks.numTracks; i++) {
        var track = sequence.videoTracks[i];
        for (var j = 0; j < track.clips.numItems; j++) {
            var clip = track.clips[j];
            // Get the in and out points of the clip (i.e: if the track has been trimmed)
            var inPoint = clip.inPoint;
            var outPoint = clip.outPoint;
            $.writeln(clip.name);
            // Print the filepath of the clip
            $.writeln(clip.projectItem.getMediaPath());
            var args = [clip.projectItem.getMediaPath()];
            var timestamps = runPythonScript(args, project.path, inPoint, outPoint); // Run the Python script
            $.writeln(timestamps);
            for (var k = 0; k < timestamps.length; k++) {
                addMarkerToClip(timestamps[k] + clip.start.seconds);
            }
        }
    }
}

main();

// alert("Blips detected and markers added to the timeline.");
