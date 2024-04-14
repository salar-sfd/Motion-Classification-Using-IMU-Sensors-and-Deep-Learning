function vectors = RotateVector(vectors, teta)
    teta_x = teta(1);
    teta_y = teta(2);
    teta_z = teta(3);   
%     quiver3(0,0,0,vectors(1),vectors(2),vectors(3),"Color",'r');
%     axis equal;
%     xlim([-1, 1]);
%     ylim([-1, 1]);
%     zlim([-1, 1]);
%     xlabel('x');
%     ylabel('y')
%     zlabel('z')
%     hold on;

    Rx = [1 0 0; 0 cos(teta_x) -sin(teta_x); 0 sin(teta_x) cos(teta_x)];
    Ry = [cos(teta_y) 0 sin(teta_y); 0 1 0; -sin(teta_y) 0 cos(teta_y)];
    Rz = [cos(teta_z) -sin(teta_z) 0; sin(teta_z) cos(teta_z) 0; 0 0 1];

    vectors = (Rz * (Ry * (Rx * vectors')))';
 
%     quiver3(0,0,0,vectors(1),vectors(2),vectors(3));
%     axis equal;
%     xlim([-1, 1]);
%     ylim([-1, 1]);
%     zlim([-1, 1]);
%     xlabel('x');
%     ylabel('y')
%     zlabel('z')
end