out = load('4out_nnr')
pose = load('4pose_nnr')
figure(1)
hold on;
grid on;
plot(out(:,:))
plot(pose,'or')
