%% Signal Generation and Resampling: verified sampling settings
% Source: https://matlabacademy.mathworks.com/details/signal-generation-and-resampling/otmlsgr
% Lesson: Signal Sampling > View Sample Points (3/3), samppts.mlx.
% Three GUI tasks received "Correct!" for (f,fs) = (1,10), (1,1.5), (2,3).
% Ungraded follow-up (3,4) finished in Academy with two outputs.
% The final Live Script source was revealed with f=3 and fs=4.
%
% Adaptation: this saved script loops over the four tested pairs and opens
% separate waveform/spectrum figures so successive plots cannot overwrite
% one another. This arrangement was not separately executed as a .m file
% during Academy verification and earns no additional exercise count.

testedPairs = [1 10; 1 1.5; 2 3; 3 4];
labels = ["Task 1", "Task 2", "Task 3", "Ungraded follow-up"];
for k = 1:size(testedPairs,1)
    f = testedPairs(k,1);
    fs = testedPairs(k,2);

    % Course waveform computation, with an independent figure added.
    tfixed = 0:1/100:100;
    yfixed = sin(2*pi*f*tfixed);
    figure('Name',char(labels(k)+" - sampled waveform"));
    plot(tfixed,yfixed);
    tmoving = 0:1/fs:100;
    ymoving = sin(2*pi*f*tmoving);
    hold on;
    movingStems = plot(tmoving,ymoving,"ro");
    movingLine = plot(tmoving,ymoving,"k--");
    hold off;
    xlim([0 10]);
    t = title("fs = "+fs+" Hz");

    % Course spectrum command, with a separate figure added.
    figure('Name',char(labels(k)+" - spectrum"));
    pspectrum(ymoving,fs);
end
